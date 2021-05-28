package case3;
import java.util.Scanner;

public class Main {
    static double manhattanDistance(double ax, double ay, double bx, double by) {
        return Math.abs(ax - bx) + Math.abs(ay - by);
    }

    public static void main(String[] args) {
        var scanner = new Scanner(System.in);
        System.out.println("Please enter x and y of point A: ");
        var ax = scanner.nextDouble();
        var ay = scanner.nextDouble();
        System.out.println("Please enter x and y of point B: ");
        var bx = scanner.nextDouble();
        var by = scanner.nextDouble();
        var res = manhattanDistance(ax, ay, bx, by);
        System.out.printf("Manhattan Distance: %.2f", res);
        var test = "dummy";
    }
}