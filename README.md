# Data Science in Production course
---

## Introduction
This is a journal-like write up to register the progress of my journey through the course. But wait, what is the "Data Science in Production" course?

It's a course designed by [Meigarom Lopes](https://github.com/Meigarom), a brazilian Data Scientist who is passionate about Data Science and for our luck (at least mine) designed this amazing course where he teaches Data Science and Machine Learning and how to deploy the model in production environment. You can get more details about the course [here](https://sejaumdatascientist.com/como-ser-um-data-scientist/) which I recommend you to do it.

So, after telling you this, let's start.

---

## The dataset
In this course, we use the [Rossmann Store Sales](https://www.kaggle.com/c/rossmann-store-sales) dataset from Kaggle. I'll leave you to check the dataset.

---

## Module 01 - Understanding the business problem
In this module, we get to understand how important is to first understand the business as a whole and find the root cause of the problem that the stakeholder want us to solve.

**Key points:**
- Understand the context.
- Spot the root cause of the problem.
- Identify the project sponsor.
- Outline the solution's key points:
  - Granularity
  - The problem type
  - Elegible methods to solve the problem
  - How it'll be delivered

In addition, we get to learn **CRISP-DS (CRoss-Industry Process - Data Science)**, a very interesting and iterable approach for Data Science projects which enable us, in each iteration, to:
- Deliver an end-to-end version of the solution.
- Have a faster value delivery.
- Map all the possible problems thay we may find during the project development.

### Problem statement
> *How might we identify the budget needed for renovations for each store?*

### Solution statement
> *We can use time series do predict the sales for each store in the next 42 days (six weeks).*

---

## Module 02 - Data description
In this module, we start getting familiar with the dataset to **understand how complex** is the problem that we are trying to solve.

**Key points:**
- Know the dataset size:
  - Do we have all the resources to start working on it?
  - Does our infrastructure support the volume of the information that we'll need to process?

- Variable types:
  - Which type os variables do we have in the dataset?
  - What is the percentage of each type?
    - Checking it helps us to choose the right techniques to manipulate the data.

- Missing values:
  - How many missing values do we have in the dataset?
  - Why there are missing values? (Issues: systems and/or manual input)
  - Depending on how critical is, we can decide whether not doing the project because there aren't enough data or use techniques to fill in the missing values.

- Summary statistics:
  - Get the **min, max, range, mean, median, standar deviation, skewness and kurtosis** values of the data for each numerical variable.
  
  ![](img/descriptive_analysis.png)
  
  - Plot box plot for categorical variables (`state_holiday`, `store_type` and `assortment` in relation to `sales`).
  
  ![](img/box_plot.png)

---

## Module 03 - Feature Engineering
In this module, we learn how to create a mindmap that helps us to **decide which variables we need** in order to validate the hypotheses and do the feature engineering. This helps in the Exploratory Data Analysis (EDA) phase.

**Key points:**
- Identify the target:
  - What are we modeling? In this case, we are modeling the daily store sales.
  
- Identify the agents:
  - Who are the agents that act on the target? (e.g. customers, stores, employees, etc.)

- Identify the agents' attributes (e.g. customer has family, age, education, locale, etc.)

![](img/hypothesis_map.png)

- Hypotheses list:
  - Outline all the hypotheses based on the mindmap and prioritize them.
  - We prioritize the hypothesis based on: whether we have or not the data at hand.
  - There may be data that we don't have it at hand and we need to spend some time on accessing it, collecting it, cleaning it and analyzing it.

- Variable filtering and variable selection:
  - Both need to be done before EDA.

  - **Variable filtering:** it is constrained to the Business. There are variables which values you will only be able to have when a business rule is triggered in the system. So, your model will not always be able to use them at hand to make predictions.

  - **Variable selection:** picking the most relevant variables for the model. Considers the correlations between variables. It does not take into account business rules.
  
---

## Module 04 - Exploratory Data Analysis (EDA)
In this module, we get to learn a lot of awesome stuff about EDA. We start to identify how the explanatory variables impact the target variable (`sales`) and what is the power of this impact. Thus, by identifying this impact we can decide to choose the right variables for our model, so it can be more assertive.

**Key points**
- The 3 goals of EDA:
  - **Understand how the business works** and how it behaves through the data.
  - **Validate/Invalidate hypotheses** and provide new information to other people.
  - **Identify which explanatory variables** impacts the target variable.

- The 3 types of EDA:
  - **Univariate analysis.**
    - How is this variable?
    - Get summary statistics (min, max, distribution, range, etc.)

  - **Bivariate analysis.**
    - How the explanatory variable impacts the target variable?
    - Get correlation between them.
    - Validate / Invalidate hypotheses.

  - **Multivariate analysis.**
    - How is the relation between the explanatory variables?
    - Get correlation between them.

### 4.1 Univariate analysis
#### 4.1.1 Target variable (`sales`)
![](img/411_target_variable_distrib.png)

#### 4.1.2 Numerical variables
![](img/412_numerical_variables_hist.png)

### 4.1.3 Categorical variable
![](img/413_categorical_variables.png)

