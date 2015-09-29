Activity(
Question("cs110/p1/1", 
     """Which of the following will print "Hello" 5 times without errors?""", 
     [
"""<pre style="width: 600px">
for (int i=0; i < 5; i++) {
    println("Hello");
}
</pre>""",
"""<pre style="width: 600px">
println("Hello");
println("Hello");
println("Hello");
println("Hello");
println("Hello");
</pre>""",
"""<pre style="width: 600px">
int i = 0;
while (i < 5) {
    println("Hello");
    i++;
}
</pre>""",
        "All of the above",
        "None of the above",
    ]),
Question("cs110/p1/2", 
     """Which of the following is a function definition?""", 
     [
"""<pre style="width: 600px">
void draw() {
}
</pre>""",
"""<pre style="width: 600px">
rect(10, 10, 50, 50);
</pre>""",
"""<pre style="width: 600px">
drawBunny(mouseX, mouseY, 50, 100);
</pre>""",
        "All of the above",
        "None of the above",
        ]
),
Question("cs110/p1/3", 
     """Which of the following has parameters?""", 
     [
"""<pre style="width: 600px">
void draw() {
}
</pre>""",
"""<pre style="width: 600px">
void drawRect(float x, float y, float w, float h) {
    rect(x, y, w, h);
}
</pre>""",
"""<pre style="width: 600px">
void drawBunny() {
    rect(10, 20, 100, 150);
}
</pre>""",
        "All of the above",
        "None of the above",
        ]
),
Question("cs110/p1/4", 
     """Which of the following is a function call?""", 
     [
"""<pre style="width: 600px">
void draw() {
}
</pre>""",
"""<pre style="width: 600px">
rect(10, 10, 50, 50);
</pre>""",
"""<pre style="width: 600px">
drawBunny(mouseX, mouseY, 50, 100);
</pre>""",
        "2 and 3",
        "None of the above",
        ]
),
    
)
