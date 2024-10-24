/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package mobemu.algorithms;

import mobemu.node.Context;
import mobemu.node.Message;
import mobemu.node.Node;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DecimalFormat;

/**
 * Class for an Epidemic node.
 *
 * Amin Vahdat and David Becker. Epidemic Routing for Partially-Connected Ad Hoc
 * Networks. Technical report, Duke University, April 2000.
 *
 * @author Radu
 */
public class Epidemic extends Node {
    public static PrintWriter writer;
    static {
        String filename = "traces/upb-hyccups2012/upb2012.csv";
        try {
            writer = new PrintWriter(new FileWriter(filename, true));
            writer.println("messageId,messageSource,messageHopCount,oldRelayId,oldFriendWithDestination,oldRelayBattery,oldCommonCommunity,oldDataMemory,newRelayId,newFriendWithDestination,newRelayBattery,newCommonCommunity,newDataMemory");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private boolean dissemination;
    private boolean altruismAnalysis;

    /**
     * Instantiates an {@code Epidemic} object.
     *
     * @param id ID of the node
     * @param nodes total number of existing nodes
     * @param context the context of this node
     * @param socialNetwork the social network as seen by this node
     * @param dataMemorySize the maximum allowed size of the data memory
     * @param exchangeHistorySize the maximum allowed size of the exchange
     * history
     * @param seed the seed for the random number generators
     * @param traceStart timestamp of the start of the trace
     * @param traceEnd timestamp of the end of the trace
     * @param dissemination {@code true} if dissemination is used, {@code false}
     * if routing is used
     * @param altruism {@code true} if altruism computations are performed,
     * {@code false} otherwise
     */
    public Epidemic(int id, int nodes, Context context, boolean[] socialNetwork, int dataMemorySize, int exchangeHistorySize,
            long seed, long traceStart, long traceEnd, boolean dissemination, boolean altruism) {
        super(id, nodes, context, socialNetwork, dataMemorySize, exchangeHistorySize, seed, traceStart, traceEnd);

        this.dissemination = dissemination;
        this.altruismAnalysis = altruism;
    }

    @Override
    public String getName() {
        return "Epidemic";
    }


    @Override
    protected void onDataExchange(Node encounteredNode, long contactDuration, long currentTime) {
        if (!(encounteredNode instanceof Epidemic)) {
            return;
        }

        Epidemic epidemicEncounteredNode = (Epidemic) encounteredNode;
        int remainingMessages = deliverDirectMessages(epidemicEncounteredNode, altruismAnalysis, contactDuration, currentTime, dissemination);
        int totalMessages = 0;

        // download each message in the encountered node's data memory that is not in the current node's memory
        for (Message message : epidemicEncounteredNode.dataMemory) {
            if (totalMessages >= remainingMessages) {
                return;
            }

            if (insertMessage(message, epidemicEncounteredNode, currentTime, altruismAnalysis, dissemination)) {
                totalMessages++;
            }

            // oldRelay.id, newRelay.id
            String messageId = "" + message.getId();
            String messageSource = "" + message.getSource();
            String messageHopCount = "" + message.getHopCount(message.getDestination());
            String oldRelayId = "" + epidemicEncounteredNode.id;
            String newRelayId = "" + this.id;
            String oldFriendWithDestination = "" + (epidemicEncounteredNode.socialNetwork[message.getDestination()] ? 1 : 0);
            String newFriendWithDestination = "" + (this.socialNetwork[message.getDestination()] ? 1 : 0);
            String oldRelayBattery = "" + epidemicEncounteredNode.getBattery().getPercentage();
            String newRelayBattery = "" + this.getBattery().getPercentage();
            // removed centrality for the moment because it is almost 0
//            DecimalFormat df = new DecimalFormat("0.000");
//            String oldRelayCentrality = df.format(epidemicEncounteredNode.getCentrality(false));
//            String newRelayCentrality = df.format(this.getCentrality(false));
//            String oldRelayLocalCentrality = df.format(epidemicEncounteredNode.getCentrality(true));
//            String newRelayLocalCentrality = df.format(this.getCentrality(true));
            String oldCommonCommunity = "" + (epidemicEncounteredNode.inLocalCommunity(message.getDestination()) ? 1 : 0);
            String newCommonCommunity = "" + (this.inLocalCommunity(message.getDestination()) ? 1 : 0);
            String oldDataMemory = "" + ((float) epidemicEncounteredNode.getDataMemorySize() / epidemicEncounteredNode.dataMemorySize);
            String newDataMemory = "" + ((float) this.getDataMemorySize() / this.dataMemorySize);

            writer.println(
                    String.join(
                            ",",
                            messageId,
                            messageSource,
                            messageHopCount,
                            oldRelayId,
                            oldFriendWithDestination,
                            oldRelayBattery,
                            oldCommonCommunity,
                            oldDataMemory,
                            newRelayId,
                            newFriendWithDestination,
                            newRelayBattery,
                            newCommonCommunity,
                            newDataMemory
                    )
            );
        }

        // download each message generated by the encountered node that is not in the current node's memory
        for (Message message : epidemicEncounteredNode.ownMessages) {
            if (totalMessages >= remainingMessages) {
                return;
            }

            if (insertMessage(message, epidemicEncounteredNode, currentTime, altruismAnalysis, dissemination)) {
                totalMessages++;
            }
        }
    }
}
