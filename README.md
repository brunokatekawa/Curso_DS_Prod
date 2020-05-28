# Data Science in Production course
---

## Table of contents
- [Module 01. Understanding the business problem](#module-01-understanding-the-business-problem)

- [Module 02. Data description](#module-02-data-description)

- [Module 03. Feature Engineering](#module-03-feature-engineering)

- [Module 04. Exploratory Data Analysis (EDA)](#module-04-exploratory-data-analysis-eda)
  - [4.1 Univariate analysis](#41-univariate-analysis)
  - [4.2 Bivariate analysis](#42-bivariate-analysis)
  - [4.3 Multivariate analysis](#43-multivariate-analysis)

---

## Introduction
This is a journal-like write up to register the progress of my journey through the course. But wait, what is the "Data Science in Production" course?

It's a course designed by [Meigarom Lopes](https://github.com/Meigarom), a brazilian Data Scientist who is passionate about Data Science and for our luck (at least mine) designed this amazing course where he teaches Data Science and Machine Learning and how to deploy the model in production environment. You can get more details about the course [here](https://sejaumdatascientist.com/como-ser-um-data-scientist/) which I recommend you to do it.

So, after telling you this, let's start.

---

## The dataset
In this course, we use the [Rossmann Store Sales](https://www.kaggle.com/c/rossmann-store-sales) dataset from Kaggle. I'll leave you to check the dataset.

---

## Module 01. Understanding the business problem
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

[back to top](#table-of-contents)

---

## Module 02. Data description
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

## Module 03. Feature Engineering
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

## Module 04. Exploratory Data Analysis (EDA)
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

As we can observe, the distribution is **moderately skewed** (`skewness = 0.641460`) and presents a **positive kurtosis** (`1.778375`) which means that we have some possible outliers in our dataset. Thus, the distribution **does not follow a normal distribution**.

As the ML algorithms requires our data to have **independent variables and normal distribution**, we can apply some techniques to do the variable transformation.

#### 4.1.2 Numerical variables
![](img/412_numerical_variables_hist.png)

Analyzing the histograms, for:
- `competition_distance`: we have more competitors that are near the stores, as they gather in the range from 0 to near 50000. 

- `competition_open_since_month`: we have a somewhat seasonal opening of competitor stores.

- `day_of_week`: we have a distribution that is nearly uniform, this tells us that the sales nearly don't vary according to the day of the week. Thus, this variable, alone, doesn't have much relevance to the model.

- `is_promo`: we have higher sales when there is no promotion (`is_promo = 0`) than when we have (`is_promo = 1`).

- `competition_open_since_year`: we can clearly see that the opening of new competitors stores had a peak near 2015.

- `customers`: as this variable describes the number of customers in a given day, we have a high concentration at the beginning then an abrupt decrease on this number. This behavior might be due to the peaked increase on the opening of new competitors stores, as the customers start to be distributed among the stores.

- `day_of_week`: as the stores are open 7 days per week, we se that there is a distribution that is nearly uniform.

- `is_promo`: we can see that there are many more stores that weren't in promotion (`is_promo = 0`) than in promotion (`is_promo = 1`).

- `open`: we can see that there are many more stores that were open (`open = 1`) than closed (`open = 0`).

- `promo`: we can see that there are many more stores that weren't in regular promotion (`promo = 0`) than those who were (`promo = 1`).

- `promo2`: we can see that there were almost equally number of stores in consecutive promotion. This might have been an experiment from Rossmann to check whether being on a consecutive promotion would impact the number of sales.

- `promo2_since_week`: we can see there is no clear pattern, there are some peaks, but we'll need to dig deeper on this topic.

- `promo2_since_year`: we can see that there were many more stores in consecutive promotion around 2014.

- `sales`: we can see that there were many more sales ranging from $0 to nearly $10,000.

- `school_holiday`: we can see that there are many more stores that weren't affected by the closure of public schools (`school_holiday = 0`) than those who were (`school_holiday = 1`).

- `store`: as this variable describes the unique Id for each store, there is no real information that we can extract from this one.

#### 4.1.3 Categorical variable
![](img/413_categorical_variables.png)

Analyzing the plots, we can see that:
- Although there are many more open stores on Easter holiday, the volume of sales is larger on Christmas. This might be due to Christmas promotion sales that stores have by the end of the year.

- For the stores of type `a`, `c` and `d` there is a high concentration of sales around $6,000. In addition, for the stores of type `b` the volume of sales is lower and its value range is much more distributed. As the provided dataset does not clearly describe the difference between the store types, it is not possible to knows whats could be generating these differences.

- For the assortment type `extended`, `basic` there is a high concentration of sales around $6,000. In addition, for the assortment `extra` the volume of sales is lower and its value range is much more distributed. This might be due the assortment of products each store have in stock and on sale which impacts the volume of sales.

<br>

### 4.2 Bivariate analysis
In this section, we validate / invalidate the hypotheses we outlined in Module 03.

#### H1. Stores with higher assortment should have higher sales.

![](img/42H1_sales_store_type.png)

We are assuming that stores that have higher assortment are classified as type `extra`. Thus, observing the bar plot, we can verify that stores with **lesser assortment (`basic`) have higher sales**.

> #### In other words, **stores with higher assortment have lesser sales**.

However, we need to check if in the past, stores with higher assortment had higher sales.

![](img/42H1_sales_yw_store_type.png)

![](img/42H1_sales_yw_store_type_extra.png)

Observing the line plots, we can verify that **stores with higher assortment (`extra`) have lesses sales**. 

> #### So, our hypothesis is **FALSE**.

In addition, as the variables have distinct behavior, it may be interesting to **include them in our ML model**.

<br>

#### H2. Stores with nearer competitors should have lesser sales.

![](img/42H2_sales_distance_comp_bars.png)

As we can observe from the bar plot, **stores with nearer competitors have higher sales**. 

> #### So, our hypothesis is **FALSE**.

![](img/42H2_sales_distance_comp_scatter.png)

We can observe from the scatter plot that we have a higher concentration of sales as we decrease the competition distance, which also makes our hypothesis **FALSE**.

**Side-by-side plots**

![](img/42H2_sales_distance_comp_grid.png)

**Correlations**

As observed in the results, the Pearson's correlation coefficient between `competition_distance` and `sales` is `-0.23` which tells us that is a **weak negative correlation**. Despite the weakness, we may include the `competition_distance` because it has a somewhat influence on the target variable (`sales`).

<br>

#### H3. Stores with longer competitors should have higher sales.
We want to know how do our `sales` behave in relation to how long a competitor store has opened.

![](img/42H3_sales_comp_time_month_bar.png)

- **Negative offset values:** we already started selling and we know when a competitor store will still open in x months. 
- **Positive offset values:** competitor store has already opened and we started selling.

As values gets near zero the higher are the sales. **The earlier the competition is, the higher the sales are.** 

> #### Thus, our hypothesis is **FALSE**.

**Side-by-side plots**

![](img/42H3_sales_comp_time_month_grid.png)

**Correlations**

As observed in the results, the Pearson's correlation coefficient between `competition_time_month` and `sales` is `-0.1` which tells us that is a **super weak negative correlation**. Despite the weakness, we may include the `competition_time_month` because it has a somewhat influence on the target variable (`sales`). We'll check its relevance later in our project.

<br>

#### H4. Stores with longer period of time in promotion should have higher sales.
As there is a lot of data, I divided the dataset in two periods: regular promotion and extended promotion.

![](img/42H4_sales_store_promo_grid.png)

As we can observe in the **Total sales x Weeks in extended promotion**, there's a period in which the extended promotion results in more sales, then after a period of time, the total sales starts to decrease.

From the **Total sales x Weeks in regular promotion**, we can observe that as the offset gets more and more near zero, the sales starts to increase.

Thus, **stores with longer period of time in promotion don't have higher sales.**, because the sales start to decrease as the promotion gets longer. 

> #### Thus, our hypothesis is **FALSE**.

**Correlations**

In addition, from the **Correlation Heatmap** we got a coefficient of `-0.029` which is pretty close to `zero`. Thus, we have a **super weak correlation**, which makes sense because looking at our data, we have long periods of almost constant total sales (see  **Total sales x Weeks in extended promotion**).

So, maybe we won't include `promo_time_week` in the model. Of course, this variable might work if we combine it with another variable, but we'll leave it for the time being.

<br>

#### H5. Stores with longer period of time in promotion should have higher sales.
As this hypothesis is similar to H4. We'll leave to validate it in the next **CRISP cycle**.

<br>

#### H6. Stores with higher consecutive promotions should have higher sales.

![](img/42H6_sales_yw_consecutive_promo.png)

Observing the results it seems that **stores with higher consecutive promotions don't have higher sales**. 

> #### Thus, our hypothesis is **FALSE**.

**Relevance**

Thinking about the relevance of the variable `promo2` to the ML model, we can say that its relevance is low. Despite the particular decrease in sales during a period, we still need a second opinion that will come from an algorithm that will aid us to decide whether we include `promo2` or not.

<br>

#### H7. Stores that open on Xmas should have higher sales.

![](img/42H6_sales_state_holiday.png)

![](img/42H6_sales_state_holiday_year.png)

As observed in the previous results, **stores that open on Xmas don't have higher sales**. 

> #### Thus, our hypothesis is **FALSE**.

One observation that we need to make here is that on year 2015, we still don't have the data from Xmas sales, because the data ends on July 31st, 2015.

In addition, as we have changes in `sales` depending on the type of `state_holiday` and which `year` is, we can consider these variables in our ML model.

<br>

#### H8. Stores should have higher sales along the years.

**Side-by-side plots**

![](img/42H6_sales_state_holiday_year_grid.png)

As observed in the previous results, stores **don't have higher sales along the years**. In addition, by observing the Pearson correlation coefficient of `-0.92`, we can verify that there is a **strong negative correlation** between `year` and `sales`. Thus, our hypothesis is **FALSE**.

<br>

#### H9. Stores should have higher sales on the second semester of the year.

**Side-by-side plots**

![](img/42H9_sales_month_grid.png)

As observed in the previous results, stores **don't have higher sales on the second semester of the year**. In addition, by observing the Pearson correlation coefficient of `-0.75`, we can verify that there is a **strong negative correlation** between `month` and `sales`. 

> #### Thus, our hypothesis is **FALSE**.

<br>

#### H10. Stores should have higher sales after the 10th day of the month.

**Side-by-side plots**

![](img/42H10_sales_day_month_grid.png)

As observed in the previous results, stores **have higher sales after the 10th day of the month**. 

> #### Thus, our hypothesis is **TRUE**.

**Correlation**

In addition, checking the Pearson's correlation coefficient, we got a value of `-0.35` which tells us that is a **no so strong correlation** between `day` and `sales`. However, as we have different values for total sales before and after the 10th day of the month, this variable **can be relevant for our ML Model**.

<br>

#### H11. Stores should have lesser sales on weekends.

**Side-by-side plots**

![](img/42H11_sales_day_week_grid.png)

**Correlation**

As observed in the previous results, stores **have lesser sales on weekends**. In addition, by observing the Pearson correlation coefficient of `-0.75`, we can verify that there is a **strong negative correlation** between `day_of_week` and `sales`. 

> #### Thus, our hypothesis is **TRUE**.

<br>

#### H12. Stores should have lesser sales during school holidays.

![](img/42H12_sales_school_holiday_bars.png)

As observed in the previous results, in general, stores **have lesser sales during school holidays, except on months of July and August**. 

> #### Thus, our hypothesis is **TRUE**.

#### 4.2.1. Hypotheses summary
| Hypothesis | Conclusion | Relavance to ML model |
| --------------- | --------------- | --------------- |
| H1 | False | Low |
| H2 | False | Medium |
| H3 | False | Medium |
| H4 | False | Low |
| H5 | (later analysis) | (later analysis) |
| H6 | False | Low |
| H7 | False | Medium |
| H8 | False | High |
| H9 | False | High |
| H10 | True | High |
| H11 | True | High |
| H12 | True | Low |

### 4.3 Multivariate analysis
In this section we'll check the correlations between the explanatory variables, separating the analysis for **numerical attributes** and **categorical attributes**.

#### 4.3.1 Numerical Attributes

![](img/432_numerical_att_corr.png)

As observed in the matrix:

| Variable A | Variable B | Correlation |
| --------------- | --------------- | --------------- |
| `day_of_week` | `open` | Medium |
| `day_of_week` | `sales` | Medium |
| `day_of_week` | `promo` | Weak |
| `day_of_week` | `school_holiday` | Weak |
| `open` | `promo` | Weak |
| `open` | `customer` | Strong |


#### 4.3.2 Categorical Attributes

To make the correlation between two categorical variables, we'll use the [Cramér V method](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V).

Please, refer to the notebook to check the calculations.

![](img/432_categorical_att_corr.png)

As observed in the results, the correlation coefficient between `store_type` and `assortment` is `0.54` which is a medium correlation and makes sense, as the bigger the store, the higher is the assortment of its products.