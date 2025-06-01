package mobemu;/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

import mobemu.algorithms.*;
import mobemu.node.Message;
import mobemu.node.Node;
import mobemu.node.Stats;
import mobemu.trace.Parser;
import mobemu.trace.Trace;
import mobemu.parsers.ParserFactory;
/**
 * Main class for MobEmu.
 *
 * @author Radu
 */



public class MobEmu {



    public static Node[] nodes;
    private static String filename = "results/" + System.getenv("ALGO").toLowerCase() + "/ALGO_" + System.getenv("ALGO") + "_TRACE_" + System.getenv("TRACE");

    static {
        if (System.getenv("MODEL") != null && !System.getenv("MODEL").isEmpty()) {
            filename += "_MODEL_" + System.getenv("MODEL");
        }

        if (System.getenv("DISSEMINATION") != null && System.getenv("DISSEMINATION").equals("true")) {
            filename += "_DISSEMINATION";
        }

        filename += ".txt";
    }
    private static void runTrace(Node[] nodes, Trace traceData, boolean batteryComputation, boolean dissemination, long seed) {

        List<Message> messages = Node.runTrace(nodes, traceData, batteryComputation, dissemination, seed);

        try (FileWriter resultFile = new FileWriter(filename, true)) {
            System.out.println("Writing to file the metrics");
            resultFile.write("Messages: " + messages.size() + "\n");
            resultFile.write(nodes[0].getName() + "\n");
            resultFile.write("HitRate " + Stats.computeHitRate(messages, nodes, dissemination) + "\n");
            resultFile.write("DeliveryCost " + Stats.computeDeliveryCost(messages, nodes, dissemination) + "\n");
            resultFile.write("DeliveryLatency " + Stats.computeDeliveryLatency(messages, nodes, dissemination) + "\n");
            resultFile.write("HopCount " + Stats.computeHopCount(messages, nodes, dissemination) + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        String chosenTrace = System.getenv("TRACE");

        Parser parser = ParserFactory.getInstance().getParser(chosenTrace);


        System.out.println("Parser: " + parser + " for trace " + chosenTrace);

        // print some trace statistics
        double duration = (double) (parser.getTraceData().getEndTime() - parser.getTraceData().getStartTime()) / (Parser.MILLIS_PER_MINUTE * 60);

        try (FileWriter resultFile = new FileWriter(filename)) {
            resultFile.write("Trace duration in hours: " + duration + "\n");
            resultFile.write("Trace contacts: " + parser.getTraceData().getContactsCount() + "\n");
            resultFile.write("Trace contacts per hour: " + (parser.getTraceData().getContactsCount() / duration) + "\n");
            resultFile.write("Nodes: " + parser.getNodesNumber() + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }


        // initialize Epidemic nodes
        long seed = 0;
        boolean dissemination = System.getenv("DISSEMINATION") != null && System.getenv("DISSEMINATION").equals("true");
        nodes = new Node[parser.getNodesNumber()];

        System.out.println("DISSEMINATION is " + dissemination);

        // epidemic
        for (int i = 0; i < nodes.length; i++) {
            if (System.getenv("ALGO").equals("EPIDEMIC")) {
                nodes[i] = new Epidemic(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), dissemination, false);
            } else if (System.getenv("ALGO").equals("SPRAY_FOCUS")) {
                nodes[i] = new SprayAndFocus(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), dissemination, false);
            } else if (System.getenv("ALGO").equals("ML_FOCUS")) {
                nodes[i] = new MlFocus(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false, dissemination);
            } else if (System.getenv("ALGO").equals("SPRINT")) {
                nodes[i] = new SPRINT(i, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false, nodes, 50);
            } else if (System.getenv("ALGO").equals("SENSE")) {
                nodes[i] = new SENSE(i, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false, nodes);
            } else if (System.getenv("ALGO").equals("IRONMAN")) {
                nodes[i] = new IRONMAN(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false);
            } else if (System.getenv("ALGO").equals("ONSIDE")) {
                nodes[i] = new ONSIDE(i, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false, nodes, 5, 5, 2, ONSIDE.ONSIDESort.CommonTopics);
            } else if (System.getenv("ALGO").equals("SAROS")) {
                nodes[i] = new SAROS(i, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), Math.random(), true, 5, (double)2/3, nodes);
            } else if (System.getenv("ALGO").equals("MOGHADAMSCHULZRINNE")) {
                nodes[i] = new MoghadamSchulzrinne(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false);
            } else if (System.getenv("ALGO").equals("SOCIALTRUST")) {
                nodes[i] = new SocialTrust(i, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                        1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), SocialTrust.FilterType.COMMON_INTERESTS, 2, true, Math.random(), true, nodes);
            }
        }


        runTrace(nodes, parser.getTraceData(), true, dissemination, seed);
        Epidemic.writer.close();
        Node.writer.close();
    }
}
