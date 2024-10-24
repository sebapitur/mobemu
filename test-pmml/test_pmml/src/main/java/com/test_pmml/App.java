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
                .load(new File("model.pmml"))
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
            

            Map<String, Double> arguments = new HashMap<>();

            arguments.put("messageHopCount", -1.391444);
            arguments.put("oldFriendWithDestination", -0.683533);
            arguments.put("oldRelayBattery", 1.283821);
            arguments.put("oldCommonCommunity", 2.060896);
            arguments.put("oldDataMemory", -1.810907);
            arguments.put("newFriendWithDestination", 1.268159);
            arguments.put("newRelayBattery", 1.073882);
            arguments.put("newCommonCommunity", -0.307097);
            arguments.put("newDataMemory", -1.907413);

            Map<String, ?> results = evaluator.evaluate(arguments);
            System.out.println(results);
            // Making the model evaluator eligible for garbage collection
            evaluator = null;

        } catch (IOException | ParserConfigurationException | SAXException | JAXBException e) {
            e.printStackTrace();
        }

    }
}
