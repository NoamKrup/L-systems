import sys
import turtle

SYSTEM_RULES = {}  # generator system rules for l-system
def derivation(axiom, steps):
    derived = [axiom]  # seed
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def rule(sequence):
    if sequence in SYSTEM_RULES:
        return SYSTEM_RULES[sequence]
    return sequence


def draw_l_system(turtle, SYSTEM_RULES, seg_length, angle):
    stack = []
    for command in SYSTEM_RULES:
        turtle.pd()
        if command in ["F", "G", "R", "L"]:
            turtle.forward(seg_length)
        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif command == "+":
            turtle.right(angle)
        elif command == "-":
            turtle.left(angle)
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)


def set_turtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Derivation")
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle

def read_from_file(file_path):
    file = open(file_path)
    line = file.readline()
    while(line.startswith("RULE : ")):
        rule = line.replace("RULE : ", "")
        key, value = rule.split("->")
        SYSTEM_RULES[key] = value
        line = file.readline()
    global axiom, ITERATIONS, SEGMENT_LENGTH, ALPHA_ZERO, ANGLE
    axiom = line.replace("AXIOM : ", "")
    ITERATIONS = file.readline().replace("ITERATIONS : ", "")
    SEGMENT_LENGTH = file.readline().replace("SEGMENT_LENGTH : ", "")
    ALPHA_ZERO = file.readline().replace("ALPHA_ZERO : ", "")
    ANGLE = file.readline().replace("ANGLE :  ", "")

def main():
    print("L - Systems")

    if len(sys.argv) >= 2 and sys.argv[1] == "-f":
        read_from_file(sys.argv[2])
    else:
        rule_num = 1
        while True:
            rule = input("Enter rule[%d]:rewrite term (0 when done): " % rule_num)
            if rule == '0':
                break
            key, value = rule.split("->")
            SYSTEM_RULES[key] = value
            rule_num += 1
        global axiom, ITERATIONS, SEGMENT_LENGTH, ALPHA_ZERO, ANGLE
        axiom = input("Enter axiom (w): ")
        ITERATIONS = int(input("Enter number of iterations (n): "))
        SEGMENT_LENGTH = int(input("Enter step size (segment length): "))
        ALPHA_ZERO = float(input("Enter initial heading (alpha-0): "))
        ANGLE = float(input("Enter angle increment (i): "))

    model = derivation(axiom, ITERATIONS)  # axiom (initial string), nth iterations
    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(ALPHA_ZERO)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    draw_l_system(r_turtle, model[-1], SEGMENT_LENGTH, ANGLE)  # draw model
    turtle_screen.exitonclick()


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        sys.exit(0)

