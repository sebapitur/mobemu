/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package mobemu.algorithms;

import jakarta.xml.bind.JAXBException;
import mobemu.node.Context;
import mobemu.node.Message;
import mobemu.node.Node;
import org.jpmml.evaluator.Evaluator;
import org.jpmml.evaluator.EvaluatorUtil;
import org.jpmml.evaluator.LoadingModelEvaluatorBuilder;
import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.io.InputStream;
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
public class MlFocus extends Node {

    private final boolean altruismAnalysis;

    private boolean dissemination;

    private static Evaluator evaluator;

    static {
        try {
            String modelName = "model-" + System.getenv("MODEL") ;

            if (System.getenv("DISSEMINATION").equals("true")) {
                modelName += "_dissemination";
            }

            modelName += ".pmml";
            System.out.println("Looking for model file: " + modelName);

            // Try to load directly from the root of the JAR
            InputStream modelStream = Thread.currentThread().getContextClassLoader().getResourceAsStream(modelName);

            if (modelStream == null) {
                System.out.println("Failed to find " + modelName + " in JAR root");
                throw new RuntimeException("Could not find model " + modelName + " in resources");
            }

            System.out.println("Successfully found " + modelName);

            evaluator = new LoadingModelEvaluatorBuilder()
                    .load(modelStream)
                    .build();

            System.out.println("Loaded Evaluator successfully");
        } catch (ParserConfigurationException | SAXException | JAXBException e) {
            URL modelUrl = MlFocus.class.getClassLoader().getResource("model-" + System.getenv("MODEL") + ".pmml");
            if (modelUrl == null) {
                throw new RuntimeException("Could not find model " + System.getenv("MODEL") + " in resources");
            }
            try {
                evaluator = new LoadingModelEvaluatorBuilder()
                        .load(new File(modelUrl.toURI())).build();
            } catch (IOException | ParserConfigurationException | SAXException | JAXBException |
                     URISyntaxException ex) {
                throw new RuntimeException(ex);
            }
            System.out.println("Loaded Evaluator successfully");
        }
    }

    /**
     * Instantiates a {@code MlFocus} object.
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
    public MlFocus(int id, int nodes, Context context, boolean[] socialNetwork, int dataMemorySize, int exchangeHistorySize,
                   long seed, long traceStart, long traceEnd, boolean altruism, boolean dissemination) {
        super(id, nodes, context, socialNetwork, dataMemorySize, exchangeHistorySize, seed, traceStart, traceEnd);
        this.altruismAnalysis = altruism;
        this.dissemination = true;
    }


    @Override
    public String getName() {
        return "MlFocus";
    }

    @Override
    protected void onDataExchange(Node encounteredNode, long contactDuration, long currentTime) {
        if (!(encounteredNode instanceof MlFocus)) {
            return;
        }

        MlFocus mlFocusEncounteredNode = (MlFocus) encounteredNode;
        int remainingMessages = deliverDirectMessages(mlFocusEncounteredNode, altruismAnalysis, contactDuration, currentTime, dissemination);
        int totalMessages = 0;
        List<Message> toRemove = new ArrayList<>();

        // download each message in the encountered node's data memory that is not in the current node's memory
        for (Message message : mlFocusEncounteredNode.dataMemory) {
            if (totalMessages >= remainingMessages) {
                return;
            }

            if (!runMlfocus(message, mlFocusEncounteredNode, toRemove, currentTime)) {
                continue;
            }

            if (insertMessage(message, mlFocusEncounteredNode, currentTime, altruismAnalysis, dissemination)) {
                totalMessages++;
            }
        }

        for (Message message : toRemove) {
            mlFocusEncounteredNode.removeMessage(message, true);
        }
        toRemove.clear();

        // download each message generated by the encountered node that is not in the current node's memory
        for (Message message : mlFocusEncounteredNode.ownMessages) {
            if (totalMessages >= remainingMessages) {
                return;
            }

            if (!runMlfocus(message, mlFocusEncounteredNode, toRemove, currentTime)) {
                continue;
            }

            if (insertMessage(message, mlFocusEncounteredNode, currentTime, altruismAnalysis, dissemination)) {
                totalMessages++;
            }
        }

        for (Message message : toRemove) {
            mlFocusEncounteredNode.removeMessage(message, false);
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
    private boolean runMlfocus(Message message, MlFocus encounteredNode, List<Message> toRemove, long currentTime) {
        // if a single message copy is left, perform the Focus phase
        if (message.getCopies(encounteredNode.id) == 1) {
            // run the ML algorithm to find out if the encountered node is a better relay than the current
            Map<String, Object> arguments = new HashMap<>();

            if (!this.dissemination) {
                arguments.put("messageHopCount", message.getHopCount(message.getDestination()));
            }

            Integer oldFriendWithDestination = 0;
            Integer newFriendWithDestination = 0;
            Integer oldCommonCommunity = 0;
            Integer newCommonCommunity = 0;

            // for the dissemination case the variable is not what the name says :)
            if (message.getDestination() == -1) {
                oldFriendWithDestination = this.getNumberOfFriendsInterestedInTopic(message.getTags().getTopics(), currentTime);
                newFriendWithDestination = encounteredNode.getNumberOfFriendsInterestedInTopic(message.getTags().getTopics(), currentTime);
                oldCommonCommunity = this.getSameCommunityNodesInterestedInTopic(message.getTags().getTopics(), currentTime);
                newCommonCommunity = encounteredNode.getSameCommunityNodesInterestedInTopic(message.getTags().getTopics(), currentTime);
            } else {
                newFriendWithDestination = encounteredNode.socialNetwork[message.getDestination()]  ? 1 : 0;
                oldFriendWithDestination = this.socialNetwork[message.getDestination()] ? 1 : 0;
                oldCommonCommunity = this.inLocalCommunity(message.getDestination()) ? 1 : 0;
                newCommonCommunity = encounteredNode.inLocalCommunity(message.getDestination()) ? 1 : 0;
            }

            arguments.put("newFriendWithDestination", newFriendWithDestination);
            arguments.put("oldFriendWithDestination", oldFriendWithDestination);
            arguments.put("newCommonCommunity", newCommonCommunity);
            arguments.put("oldCommonCommunity", oldCommonCommunity);

            arguments.put("oldRelayBattery", this.getBattery().getPercentage());
            arguments.put("oldDataMemory", (float)(this.getDataMemorySize() / this.dataMemorySize));

            arguments.put("newRelayBattery", encounteredNode.getBattery().getPercentage());
            arguments.put("newDataMemory", (float)(encounteredNode.getDataMemorySize() / this.dataMemorySize));

            var results = evaluator.evaluate(arguments);

            int finalResult = (int)EvaluatorUtil.decodeAll(results).get(evaluator.getTargetFields().get(0).getName());
            // if the node that doesn't have the message is the better one (has met
            // the destination more recently plus delta), transfer the message
            if (finalResult == 1) {
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
