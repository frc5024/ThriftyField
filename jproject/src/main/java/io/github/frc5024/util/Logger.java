package io.github.frc5024.util;

public class Logger {

    public static void log(String component, String message) {
        System.out.println(String.format("[%s] %s", component, message));
    }
}