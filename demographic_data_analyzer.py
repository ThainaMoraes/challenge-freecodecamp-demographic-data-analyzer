import pandas as pd


def calculate_demographic_data(print_data=True):
    
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    search = [df[df['race'] == race]['race'].count() for race in df.race.unique()]
    race_count = pd.Series(search, index = df.race.unique())

    # What is the average age of men?
    average_age_men = round(df.query('sex == "Male"')['age'].mean(),1)
  
    # What is the percentage of people who have a Bachelor's degree?
    bachelors_degree = df.query('education == "Bachelors"').count()[0]
    all_degree  = df.count()[0]
    percentage_bachelors = round(bachelors_degree/all_degree*100,1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    advanced_education_list = ['Bachelors', 'Masters', 'Doctorate']

    df_higher_education = df.loc[df['education'].isin(advanced_education_list)]
    df_higher_education_rich = df_higher_education.query("salary == '>50K'")

    count_higher_education = df_higher_education.count()[0]
    count_higher_education_rich = df_higher_education_rich.count()[0]

    not_advanced_education_list = ['HS-grad', '11th', '9th', 'Some-college','Assoc-acdm', 'Assoc-voc', '7th-8th', 'Prof-school', '5th-6th', '10th', '1st-4th', 'Preschool', '12th']
    df_lower_education = df.loc[df['education'].isin(not_advanced_education_list)]

    df_lower_education_rich = df_lower_education.query("salary == '>50K'")
    
    count_lower_education = df_lower_education.count()[0]
    count_lower_education_rich = df_lower_education_rich.count()[0]

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = round(count_higher_education/df.count()[0]*100,1)
    lower_education = round(count_lower_education/df.count()[0]*100,1)

    # percentage with salary >50K
    higher_education_rich = round(count_higher_education_rich/count_higher_education*100,1)
    lower_education_rich = round(count_lower_education_rich/count_lower_education*100,1)
    
    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours =  df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    df_num_min_workers = df[df['hours-per-week'] == 1]
    num_min_workers = df_num_min_workers.query("salary == '>50K'").count()[0]

    rich_percentage = round(num_min_workers/df_num_min_workers.count()[0]*100,1)

    # What country has the highest percentage of people that earn >50K?
    df_group1 = df[['salary','native-country']].groupby('native-country').count()
    df_group1.rename(columns = {'salary':'all'},inplace = True)
    
    df_salary = df.query('salary == ">50K"')
    df_group2 = df_salary[['salary','native-country']].groupby('native-country').count()
    df_group2.rename(columns = {'salary':'rich'},inplace = True)

    result = df_group1.join(df_group2)
    result['percentage'] = round(result['rich']/result['all']*100,1)
    result.sort_values('percentage',ascending=False, inplace = True)
    
    highest_earning_country = result.iloc[0].name
    highest_earning_country_percentage = result.iloc[0]['percentage']
  
    #Identify the most popular occupation for those who earn >50K in India.
  
    df_india_salary = df[df['native-country'] == 'India'].query('salary == ">50K"')
    df_india_salary['occupation'].unique()

    df_group_india = df_india_salary.groupby('occupation').count()[['salary']].sort_values('salary', ascending= False)
    
    top_IN_occupation = df_group_india.iloc[0].name
  
    # DO NOT MODIFY BELOW THIS LINE
  
    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)
      
    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':         highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
        
    }