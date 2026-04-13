# Datasheet

This datasheet documents the task dataset for Computer Use Agents (CUAs) introduced in this work. The dataset is intended to support three use cases: evaluation of autonomous evaluators, fine-tuning of CUAs, and training of CUA systems.

The dataset is available on Zenodo: [link placeholder].

---

Motivation
----------

-   **For what purpose was the dataset created?** Was there a specific
    task in mind? Was there a specific gap that needed to be filled?
    Please provide a description.

    The dataset was created for two purposes:
    1. Evaluating the reliability of autonomous evaluators for CUAs (`evaluation` split)
    2. Training and fine-tuning of CUAs (`learning` split)
    
    The dataset covers three operating systems: Windows, Linux, and macOS. To the best of our knowledge, no previous dataset has provided such broad coverage across both operating systems and applications.

Composition
-----------

-   **What do the instances that comprise the dataset represent (e.g.,
    documents, photos, people, countries)?** Are there multiple types of
    instances (e.g., movies, users, and ratings; people and interactions
    between them; nodes and edges)? Please provide a description.

    Each instance consists of task-related data necessary for either evaluation or training.
    For `evaluation` split this include:
    
    1. Task description (text)
    2. OS specification (Windows, Linux or macOS)
    3. Application name
    4. Trajectory data (that includes step-by-step screenshots and actions of the agent's performing the task)
    5. Ground truth label (`done` or `not done`) - whether the agent has succesfuly done the intended task; human labeled

    And for `learning` split:
    1. Task description (text)
    2. OS specification (Windows, Linux or macOS)
    3. Application name

-   **How many instances are there in total (of each type, if
    appropriate)?**

    The dataset includes 42 applications for each OS, with 60 tasks for each application, resulting with 2520 tasks for each OS and 7560 tasks in total.
    The `evaluation` split includes 20 tasks per aplication ($\frac{1}{3}$ of the dataset); `learning` split has 40 tasks per application ($\frac{2}{3}$ of the dataset).



-   **Are relationships between individual instances made explicit
    (e.g., users' movie ratings, social network links)?** If so, please
    describe how these relationships are made explicit.

    Our dataset contain no relationships between
    different tasks. 

-   **Are there recommended data splits (e.g., training,
    development/validation, testing)?** If so, please provide a
    description of these splits, explaining the rationale behind them.

    The dataset is already splitted into `evaluation` and `learning` parts. The validation/testing splits can be decided by user.



-   **Does the dataset contain data that might be considered
    confidential (e.g., data that is protected by legal privilege or by
    doctor patient confidentiality, data that includes the content of
    individuals' non-public communications)?** If so, please provide a
    description.

    No.

-   **Does the dataset contain data that, if viewed directly, might be
    offensive, insulting, threatening, or might otherwise cause
    anxiety?** If so, please describe why.

    No.

-   **Does the dataset relate to people?** If not, you may skip the
    remaining questions in this section.

    No.


-   **Any other comments?**

    No.

Collection process
------------------

-   **How was the data associated with each instance acquired?** Was the
    data directly observable (e.g., raw text, movie ratings), reported
    by subjects (e.g., survey responses), or indirectly inferred/derived
    from other data (e.g., part-of-speech tags, model-based guesses for
    age or language)? If data was reported by subjects or indirectly
    inferred/derived from other data, was the data validated/verified?
    If so, please describe how.

    The tasks descriptions were partially synthetically generated. The trajectories for the `evaluation` split were got by running UI-TARS agent, and recording it's corresponding trajectories.
    The labels `done`/`not done` for the `evaluation` split were manually labeled.

-   **What mechanisms or procedures were used to collect the data (e.g.,
    hardware apparatus or sensor, manual human curation, software
    program, software API)?** How were these mechanisms or procedures
    validated?

    To gather the tasks trajectorues of UI-TARS agent, we used [UTM](https://mac.getutm.app/) virtual machine.





-   **Does the dataset relate to people? If not, you may skip the
    remainder of the questions in this section.**

    No.

-   **Any other comments?**

    No.


Uses
----

-   **Has the dataset been used for any tasks already?** If so, please
    provide a description.

    In the thesis, we used the dataset for the following 

-   **Is there a repository that links to any or all papers or systems
    that use the dataset?** If so, please provide a link or other access
    point.

    This [repository] (https://github.com/martasumyk/cua-eval-and-finetuning) contains all the code for evaluation and fine-tuning done with this dataset.

-   **What (other) tasks could the dataset be used for?**

    The dataset can be also used for training CUAs from scratch.


-   **Any other comments?**

    No.

Distribution
------------

-   **How will the dataset will be distributed (e.g., tarball on
    website, API, GitHub)?** Does the dataset have a digital object
    identifier (DOI)?

    The dataset will be be distributed via Zenodo, see
    [link placeholder]. The dataset will have a DOI.


-   **Will the dataset be distributed under a copyright or other
    intellectual property (IP) license, and/or under applicable terms of
    use (ToU)?** If so, please describe this license and/or ToU, and
    provide a link or other access point to, or otherwise reproduce, any
    relevant licensing terms or ToU, as well as any fees associated with
    these restrictions.

    To-do 


-   **Any other comments?**

    No.


