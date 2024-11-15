/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package mobemu;

import java.util.*;
import mobemu.algorithms.Epidemic;
import mobemu.algorithms.MlFocus;
import mobemu.node.Message;
import mobemu.node.Node;
import mobemu.node.Stats;
import mobemu.parsers.UPB;
import mobemu.trace.Parser;
import mobemu.trace.Trace;
/**
 * Main class for MobEmu.
 *
 * @author Radu
 */

import org.jpmml.evaluator.LoadingModelEvaluatorBuilder;
import org.jpmml.evaluator.Evaluator;

public class MobEmu {

    private static void runTrace(Node[] nodes, Trace traceData, boolean batteryComputation, boolean dissemination, long seed) {
        LoadingModelEvaluatorBuilder evaluator = new LoadingModelEvaluatorBuilder();
        System.out.println("Loaded evaluator");

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
//        Parser parser = new UPB(UPB.UpbTrace.UPB2011);
        Parser parser = new UPB(UPB.UpbTrace.UPB2012);

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
//        for (int i = 0; i < nodes.length; i++) {
//            nodes[i] = new Epidemic(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
//                    1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), dissemination, false);
//        }

        for (int i = 0; i < nodes.length; i++) {
            nodes[i] = new MlFocus(i, nodes.length, parser.getContextData().get(i), parser.getSocialNetwork()[i],
                    1000, 50, seed, parser.getTraceData().getStartTime(), parser.getTraceData().getEndTime(), false);
        }

        runTrace(nodes, parser.getTraceData(), false, dissemination, seed);




        Epidemic.writer.close();
        Node.writer.close();
    }
}
