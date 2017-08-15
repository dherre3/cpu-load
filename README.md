# CPU LOAD EXPERIMENTS

This experiment, pertains to the systematic error that the CPU load introduces in running benchmarks. 
### Introduction
A CPU normally works by scheduling using a priority queue, a given process is given a "quanta" of time in every cycle before is it placed back on the queue. This means than rather than running tasks in a serial fashion, the task or processes are run in an interleaved fashion. Each of these processes, therefore, has two associated times with it.  i.e. user time, and system time. Both of them describe how long the cpu spends running a given process. The user time describes how long the cpu spent running the actual process. On the other hand, the system time, refers to the time the cpu spent context switching between different processes. 
As a consequence of this process, intuitively, if there are more tasks to run, those tasks will take more absolute time, due to the cpu switching between them.
This study aims to answer the following question:
    - Does the cpu load affect a running benchmark in a significant way? 
    - Can the time induced by the cpu load introduce a noticeable systematic error into measurement, or is it part of a random error associated with it?
    - As experimenters, how can we control such a situation? 
    - When does the cpu load become relevant when measuring a benchmark?


