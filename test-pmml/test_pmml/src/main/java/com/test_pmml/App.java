package com.test_pmml;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import javax.xml.parsers.ParserConfigurationException;

import org.jpmml.evaluator.OutputField;
import org.jpmml.evaluator.Evaluator;
import org.jpmml.evaluator.EvaluatorUtil;
import org.jpmml.evaluator.InputField;
import org.jpmml.evaluator.LoadingModelEvaluatorBuilder;
import org.jpmml.evaluator.ModelEvaluator;
import org.jpmml.evaluator.TargetField;
import org.xml.sax.SAXException;
import org.jpmml.evaluator.neural_network.NeuralNetworkEvaluator;
import jakarta.xml.bind.JAXBException;

/**
 * Hello world!
 */
public final class App {
    private App() {
    }

    /**
     * Says hello to the world.
     * @param args The arguments of the program.
     */
    public static void main(String[] args) {
        try {
            System.out.println("Working Directory = " + System.getProperty("user.dir"));
            Evaluator evaluator = new LoadingModelEvaluatorBuilder()
                .load(new File("C:/Users/sebastian.pitur/Documents/facultate/mobemu/src/main/resources/model-rf-Haggle-Content.pmml"))
                .build();
                // Perforing the self-check
            evaluator.verify();

            // Printing input (x1, x2, .., xn) fields
            List<InputField> inputFields = evaluator.getInputFields();
            System.out.println("Input fields: " + inputFields);

            // Printing secondary result (eg. probability(y), decision(y)) fields
            List<OutputField> outputFields = evaluator.getOutputFields();
            System.out.println("Output fields: " + outputFields);


            Map<String, Object> arguments = new HashMap<>();


            {oldDataMemory=0.0, oldFriendWithDestination=0, oldRelayBattery=0.012039829745041225, newDataMemory=0.0, newCommonCommunity=0, newFriendWithDestination=0, oldCommonCommunity=0, newRelayBattery=0.015421102090962664}

            arguments.put("messageHopCount", 0);
            arguments.put("oldFriendWithDestination", 1);
            arguments.put("oldRelayBattery", 0.38);
            arguments.put("oldCommonCommunity", 0);
            arguments.put("oldDataMemory", 0.57);
            arguments.put("newFriendWithDestination", 1);
            arguments.put("newRelayBattery", 0.24);
            arguments.put("newCommonCommunity", 0);
            arguments.put("newDataMemory", 0.58);
            System.out.println(evaluator.evaluate(arguments));
            Object y = EvaluatorUtil.decodeAll(evaluator.evaluate(arguments)).get(evaluator.getTargetFields().get(0).getName());
            System.out.println(EvaluatorUtil.decodeAll(evaluator.evaluate(arguments)).get(evaluator.getTargetFields().get(0).getName()));

        } catch (IOException | ParserConfigurationException | SAXException | JAXBException e) {
            e.printStackTrace();
        }

    }
}
