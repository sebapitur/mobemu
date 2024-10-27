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
import org.jpmml.evaluator.TargetField;
import org.xml.sax.SAXException;

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
            Evaluator evaluator = new LoadingModelEvaluatorBuilder()
                .load(new File("model-svm.pmml"))
                .build();
                // Perforing the self-check
            evaluator.verify();

            // Printing input (x1, x2, .., xn) fields
            List<InputField> inputFields = evaluator.getInputFields();
            System.out.println("Input fields: " + inputFields);

            // Printing primary result (y) field(s)
            List<TargetField> targetFields = evaluator.getTargetFields();
            System.out.println("Target field(s): " + targetFields);

            // Printing secondary result (eg. probability(y), decision(y)) fields
            List<OutputField> outputFields = evaluator.getOutputFields();
            System.out.println("Output fields: " + outputFields);
            

            Map<String, Object> arguments = new HashMap<>();

            arguments.put("messageHopCount", 0);
            arguments.put("oldFriendWithDestination", 1);
            arguments.put("oldRelayBattery", 0.38);
            arguments.put("oldCommonCommunity", 0);
            arguments.put("oldDataMemory", 0.57);
            arguments.put("newFriendWithDestination", 1);
            arguments.put("newRelayBattery", 0.24);
            arguments.put("newCommonCommunity", 0);
            arguments.put("newDataMemory", 0.58);

            Map<String, ?> results = evaluator.evaluate(arguments);
            System.out.println(results);
            // Making the model evaluator eligible for garbage collection
            evaluator = null;

        } catch (IOException | ParserConfigurationException | SAXException | JAXBException e) {
            e.printStackTrace();
        }

    }
}
