<h1> Trace Editor </h1>

<p>
To run, access the trace-editor py in the root directory. <br />
Please use the correct input for now, I haven't put any advanced validation. <br />

Before running, create 2 symlinks/folders inside this directory: <br />
./in: contains all input files <br />
./out: contains all output files <br />
<br />
The scripts will take every input and produce every output to those directories. <br />
</p>

<h2>List of commands: </h2>
<p>
1. Preprocess a trace <br />
</p>
<pre>python trace-editor.py -file &lt;tracename&gt; -preprocess (-filter read/write)</pre>

<p>
2. Modify a trace (Precondition: The trace must have been preprocessed)<br />
Resize all requests size by 2x and rerate all request arrival time by 0.5x : <br />
</p>
<pre>python trace-editor.py -file &lt;tracename&gt; -resize 2 -rerate 0.5</pre>

<p>
3. Filter to RAID-0 disk
In this example get the disk 0 from 4 disks with the stripe unit size 65536 bytes
</p>

<pre>python trace-editor.py -filterraid -file &lt;infile&gt; -ndisk 4 -odisk 0 -stripe 65536</pre>

<p>
4. Check IO imbalance in the RAID Disks
This example uses 3disks with the granularity of 300seconds.
</p>

<pre>python trace-editor.py -ioimbalance -files &lt;disk0&gt;.trace &lt;disk1&gt;.trace &lt;disk2&gt;.trace -granularity 300</pre>

<p>
5. Check the busiest or the most loaded (in kB) time for a specific disk in a directory (before preprocessed) <br />
<b>Still in improvement</b>, right now, this command will first combine all traces inside a directory. <br />
Make sure that all traces are well ordered based on their time (check with ls to make sure). <br />
If the traces are not ordered, please rename the traces first, the script will just take all traces <br />
by assuming that all of them are already sorted. <br />
<br />
Notes: <br />
duration - in hrs, in this example 1hrs <br />
top - top n result in this example 3 top results <br />
</p>
<pre>python trace-editor.py -dir &lt;dirname&gt; -mostLoaded -duration 1 -top 3</pre>
<pre>python trace-editor.py -dir &lt;dirname&gt; -busiest -duration 1 -top 3</pre>
<pre></pre>


