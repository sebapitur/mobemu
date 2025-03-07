/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package mobemu.algorithms;

import java.util.*;

import mobemu.MobEmu;
import mobemu.node.*;

/**
 * Class for a Spray and Focus node.
 *
 * Thrasyvoulos Spyropoulos, Konstantinos Psounis, and Cauligi S. Raghavendra.
 * Spray and focus: Efficient mobility-assisted routing for heterogeneous and
 * correlated mobility. Fifth Annual IEEE International Conference on Pervasive
 * Computing and Communications Workshops, 2007. PerCom Workshops' 07, pp.
 * 79-85. IEEE, 2007.
 *
 * @author Radu
 */
public class SprayAndFocus extends Node {

    private final boolean altruismAnalysis;
    private boolean dissemination;
    private final long delta;

    /**
     * Default delta value.
     */
    private static final long DEFAULT_DELTA = 1000;

    /**
     * Instantiates a {@code SprayAndFocus} object.
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
     * @param altruism {@code true} if altruism computations are performed,
     * {@code false} otherwise
     */
    public SprayAndFocus(int id, int nodes, Context context, boolean[] socialNetwork, int dataMemorySize, int exchangeHistorySize,
            long seed, long traceStart, long traceEnd, boolean dissemination, boolean altruism) {
        this(id, nodes, context, socialNetwork, dataMemorySize, exchangeHistorySize, seed, traceStart, traceEnd, altruism, DEFAULT_DELTA);
        this.dissemination = dissemination;
    }

    /**
     * Instantiates a {@code SprayAndFocus} object.
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
     * @param altruism {@code true} if altruism computations are performed,
     * {@code false} otherwise
     * @param delta minimum difference between encounter times for message
     * transfer
     */
    public SprayAndFocus(int id, int nodes, Context context, boolean[] socialNetwork, int dataMemorySize, int exchangeHistorySize,
            long seed, long traceStart, long traceEnd, boolean altruism, long delta) {
        super(id, nodes, context, socialNetwork, dataMemorySize, exchangeHistorySize, seed, traceStart, traceEnd);

        this.altruismAnalysis = altruism;
        this.delta = delta;
    }

    @Override
    public String getName() {
        return "Spray and Focus";
    }

    @Override
    protected void onDataExchange(Node encounteredNode, long contactDuration, long currentTime) {
        if (!(encounteredNode instanceof SprayAndFocus)) {
            return;
        }

        SprayAndFocus sprayAndFocusEncounteredNode = (SprayAndFocus) encounteredNode;
        int remainingMessages = deliverDirectMessages(sprayAndFocusEncounteredNode, altruismAnalysis, contactDuration, currentTime, dissemination);
        int totalMessages = 0;
        List<Message> toRemove = new ArrayList<>();

        // download each message in the encountered node's data memory that is not in the current node's memory
        for (Message message : sprayAndFocusEncounteredNode.dataMemory) {
            if (totalMessages >= remainingMessages) {
                return;
            }

            if (!runSprayAndFocus(message, sprayAndFocusEncounteredNode, toRemove, currentTime)) {
                continue;
            }

            if (insertMessage(message, sprayAndFocusEncounteredNode, currentTime, altruismAnalysis, dissemination)) {
                totalMessages++;
            }
        }
        
        for (Message message : toRemove) {
            sprayAndFocusEncounteredNode.removeMessage(message, true);
        }
        toRemove.clear();

        // download each message generated by the encountered node that is not in the current node's memory
        for (Message message : sprayAndFocusEncounteredNode.ownMessages) {
            if (totalMessages >= remainingMessages) {
                return;
            }

            if (!runSprayAndFocus(message, sprayAndFocusEncounteredNode, toRemove, currentTime)) {
                continue;
            }

            if (insertMessage(message, sprayAndFocusEncounteredNode, currentTime, altruismAnalysis, dissemination)) {
                totalMessages++;
            }
        }
        
        for (Message message : toRemove) {
            sprayAndFocusEncounteredNode.removeMessage(message, false);
        }
        toRemove.clear();
    }

    /**
     * Spray and Focus algorithm.
     *
     * @param message message to be analyzed
     * @param encounteredNode encountered node
     * @return {@code true} if the message should be copied, {@code false}
     * otherwise
     */
    private boolean runSprayAndFocus(Message message, SprayAndFocus encounteredNode, List<Message> toRemove, long currentTime) {
        // if a single message copy is left, perform the Focus phase
        if (message.getCopies(encounteredNode.id) == 1) {
            // compute the last time each of the two nodes encountered the message's destination
            long timeDestinationSeen = Long.MIN_VALUE;
            long timeDestinationSeenEncountered = Long.MIN_VALUE;

            if (!dissemination) {
                ContactInfo info = encounteredNodes.get(message.getDestination());

                if (info != null) {
                    timeDestinationSeen = info.getLastEncounterTime();
                }
            } else {
                timeDestinationSeen = this.getMaxEncounterTimeWithTopic(message, currentTime);
            }


            if (!dissemination) {
                ContactInfo info = encounteredNode.encounteredNodes.get(message.getDestination());

                if (info != null) {
                    timeDestinationSeenEncountered = info.getLastEncounterTime();
                }
            } else {
                timeDestinationSeenEncountered = encounteredNode.getMaxEncounterTimeWithTopic(message, currentTime);
            }

            // if the node that doesn't have the message is the better one (has met
            // the destination more recently plus delta), transfer the message
            if (timeDestinationSeen > timeDestinationSeenEncountered + delta) {
                //encounteredNode.removeMessage(message, fromDataMemory);
                toRemove.add(message);
                return true;
            }

            return false;
        }

        // if the current node doesn't contain the message, it receives
        // half of the copies of the message from the encountered node
        if (!dataMemory.contains(message) && !ownMessages.contains(message)) {
            message.setCopies(encounteredNode.id, message.getCopies(encounteredNode.id) / 2);
            message.setCopies(id, message.getCopies(encounteredNode.id));
        }

        return true;
    }
}
