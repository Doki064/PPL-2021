package case6;

import java.util.Scanner;

public class Main {
    static double circleArea(double r) {
        return Math.PI * Math.pow(r, 2);
    }

    public static void main(String[] args) {
        var scanner = new Scanner(System.in);
        var r = scanner.nextDouble();
        int a;
        int b;
        int c;
        int d;
        int z = a + (c + d);
<<<<<<< HEAD
        if (r <= 0) {
            System.out.println("Circle radius must be positive");
        } else {
            var res = areaCircle(r); // somehow function name is reversed here
            System.out.printf("Circle area: %.2f", res);
        }
        scanner.close();
=======
        int y = (a + b) * c;
        int x = d / b;
        int Quang = (a + an_undefined_variable_come_out_of_some_where) + (c + d);
        System.out.printf("Hello world");
>>>>>>> eb3f26cc7916253b6b9ba35678d1d1f8d449c40a
    }
}