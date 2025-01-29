/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package mobemu;

import java.rmi.ServerError;
import java.util.*;
import mobemu.algorithms.Epidemic;
import mobemu.algorithms.MlFocus;
import mobemu.algorithms.SprayAndFocus;
import mobemu.node.Message;
import mobemu.node.Node;
import mobemu.node.Stats;
import mobemu.parsers.UPB;
import mobemu.trace.Parser;
import mobemu.trace.Trace;
import mobemu.parsers.ParserFactory;
/**
 * Main class for MobEmu.
 *
 * @author Radu
 */

import org.jpmml.evaluator.LoadingModelEvaluatorBuilder;
import org.jpmml.evaluator.Evaluator;

public class MobEmu {

    private static void runTrace(Node[] nodes, Trace traceData, boolean batteryComputation, boolean dissemination, long seed) {
        List<Message> messages = Node.runTrace(nodes, traceData, batteryComputation, dissemination, seed);
        System.out.println("Messages: " + messages.size());

        // print opportunistic algorithm statistics
        System.out.println(nodes[0].getName());
        System.out.println("HitRate " + Stats.computeHitRate(messages, nodes, dissemination));
        System.out.println("DeliveryCost " + Stats.computeDeliveryCost(messages, nodes, dissemination));
        System.out.println("DeliveryLatency " + Stats.computeDeliveryLatency(messages, nodes, dissemination));
        System.out.println("HopCount " + Stats.computeHopCount(messages, nodes, dissemination));
    }
    public static void main(String[] args) {
        String chosenTrace = System.getenv("TRACE");

//        try {
            Parser parser = ParserFactory.getInstance().getParser(chosenTrace);
            // print some trace statistics
            double duration = (double) (parser.getTraceData().getEndTime() - parser.getTraceData().getStartTime()) / (Parser.MILLIS_PER_MINUTE * 60);
            System.out.println("Trace duration in hours: " + duration);
            System.out.println("Trace contacts: " + parser.getTraceData().getContactsCount());
            System.out.println("Trace contacts per hour: " + (parser.getTraceData().getContactsCount() / duration));
            System.out.println("Nodes: " + parser.getNodesNumber());

            // initialize Epidemic nodes
            long seed = 0;
            boolean dissemination = false;
            Node[] nodes = new Node[parser.getNodesNumber()];


            // epidemic
            for (int i = 0; i < nodes.length; i++) {
                if (System.getenv("ALGO").equals("EPIDEMIC")) {
                    nodes[i] = new Epidemic(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                            1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), dissemination, false);
                } else if (System.getenv("ALGO").equals("SPRAY_FOCUS")) {
                    nodes[i] = new SprayAndFocus(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                            1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false);
                } else if (System.getenv("ALGO").equals("ML_FOCUS")) {
                    nodes[i] = new MlFocus(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                            1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false);
                }
            }


            runTrace(nodes, parser.getTraceData(), false, dissemination, seed);
            Epidemic.writer.close();
            Node.writer.close();
//        } catch (Exception e){
//            System.err.println(Arrays.toString(e.getStackTrace()));
//            System.err.println("Maybe you have not set TRACE and OUTPUT_WRITE variables");
//        }
    }
}
