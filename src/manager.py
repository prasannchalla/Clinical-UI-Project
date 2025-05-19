from user import User
import pandas as pd
import matplotlib.pyplot as plt

class Manager(User):
    def __init__(self, role, patient_record_manager):
        super().__init__(role, patient_record_manager)

    #create report
    def do_action(self):
        print(f"Current role: {self._role}")
        self.__do_generate_stat_reports_action()

    def __do_generate_stat_reports_action(self):
        # Load the dataset
        df = pd.read_csv(self._patient_record_manager.patient_file_name, parse_dates=['Visit_time'])

        # format date strings to datetime objects
        df['Visit_time'] = pd.to_datetime(df['Visit_time'])

        # EExtract motnth for grouping
        df['Visit_month'] = df['Visit_time'].dt.to_period('M').astype(str)

        # Create age group labels and bins
        bins = [0, 18, 35, 50, 65, 100]
        labels = ['0-18', '19-35', '36-50', '51-65', '66+']
        df['age_group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

        # Plotting trends
        self.__plot_graph(df, 'Gender', 'Gender')
        self.__plot_graph(df, 'Race', 'Race')
        self.__plot_graph(df, 'Ethnicity', 'Ethnicity')
        self.__plot_graph(df, 'age_group', 'Age Group')


    # Function to plot graph
    def __plot_graph(self, df, group_by_col, title):
        trend = df.groupby(['Visit_month', group_by_col])['Patient_ID'].nunique().unstack().fillna(0)
        trend.plot(kind='line', marker='o', figsize=(12, 6))
        plt.title(f"Temporal Trend of Patient Visits by {title}")
        plt.xlabel("Month")
        plt.ylabel("Number of Unique Patients")
        plt.xticks(rotation=45)
        plt.legend(title=title)
        plt.tight_layout()
        plt.grid(True)
        plt.show()




