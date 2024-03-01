# PythonCMC
## Python Common Model of Cognition Project
### The goal of this project is to create a computational architecture that can be used to implement cognitive architectures consistent with the Common Model of Cognition
PythonCMC is primarily meant as a teaching tool. In the future there may be different versions but, for now, the focus is on creating a very simple version, so that students can easily see how it works. In service of this, this version of PythonCMC focuses on using ACT-R type chunks and basic production systems. It should be noted that CMC architectures are not restricted to this sort of computational implementation.
### PythonCMC breaks down cognitive models into two levels
1. **The computational architecture**
  * In this system the computational architecture is seperated from the cognitive architecture
  * The purpose of this is to seperate the theory expressed in the cognitive architecture from the computational methods used to make it run
  * The computational architecture allows agents to *think*, to *percieve* an environment, and *act* in the environment.
  * To do this it provides a system to simulate modules acting in parallel and communicating with each other
  * This works by using production rules to alter and/or move *chunks* between *memories*.
  * In terms of Python code:
    * Chunks are dictionaries expressing propositional knowledge and containing a utility value
    * Memories are dictionaries of chunk dictionaries
    * Production rules are dictionaries that contain a chunk for matching to and an action
    * Production systems are lists of production rules 
  * Production rules have the following basic functions:
    * chunk matching
    * chunk copying
    * chunk alteration
  * Note that this means that the ways that this system is implemented makes no theoretical claims about the cognitive architecture
    *  In fact, the assumptions of the compuational architecture are explicilty not part of the cognitive architecture
    *  The only thing the choice of computational architecture implies is that it is sufficient to create a version of the cognitive architecture that is sufficient to model the task in question
2. **The cognitive architecture and model**
  * Usually the cognitive architecture and the computational architecture are combined so that the modeler just creates the model
  * This has the advantage of making clear that the cognitive architecture is fixed and that the model represents different knowledge configurations expressed as Declarative Memory chunks and Procedural Memory production rules, due to the computational architecture in this case
  * In this system the cognitive architecture is created by creating a cognitive model
  * This is done by adding in all the modules, connections between modules, and functionality assumed by the architecture, in the model
  * The cognitive architecture is built in the following way:
    1. create specific memories and production systems
    2. (optional) create additional functionality by building it into a production system
       * This is where this way of creating cognitive architectures is somewhat different. In the computational architecture, production systems do double duty. As in most cognitive models, they are used to model functionality that is believed to map onto actual neural systems that match and choose. PythonCMC also uses produciton systems in this way, to represent real cognitive activity. However, PythonCMC also uses production systems as (1) a way to to model the actions of modules and (2) a way to integrate sub symbolic processing into the architecture (so, triple duty, actually).
       * This is a coding trade off. Arguably, it makes the cognitive architecture less discernable in the code because produciton systems are used all over the place. However, it also makes the compuational architecture much simpler and easier to understand. This fits with the goals of this project, to have a computational architecture that is seperate and not optimized for any particular cognitive architecture, but rather for a class of cognitive architectures.
       * So, as in all cognitive architecture, but maybe particularly in Python CMC, it is important to add commenting to your code to make clear what is what. However, once a cognitive architecture is defined, it can be put in a sepperate bit of code and imported into PythonCMC so that these complications are hidden.
     
