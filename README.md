<h1> Trace Editor </h1>

<p>
To run, access the trace-editor py in the root directory. <br />

Please create 2 symlinks/folders inside this directory: <br />
./in: contains all input files <br />
./out: contains all output files <br />
</p>

<h2>List of commands: </h2>
<p>
1. Preprocess a trace <br />
</p>
<pre>python trace-editor.py -file &lt;tracename&gt; -preprocess (-filter read/write)</pre>
<p>
2. Modify a trace (Precondition: The trace must have been preprocessed)<br />
Resize all requests size by 2x and rerate all request arrival time by 0.5x :<br />
<pre>python trace-editor.py -file &lt;tracename&gt; -resize 2 -rerate 0.5</pre>
</p>

