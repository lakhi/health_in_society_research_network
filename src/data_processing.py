import pandas as pd

def load_and_clean_survey_data(file_path):
    return GiGSurveyDataProcessor(file_path).get_data()

class GiGSurveyDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)
        self.clean_data()

    def get_data(self):
        return self.df
    
    def clean_data(self):
        self.df.columns = self.df.columns.str.strip()
        self.__clean_department()
        self.__clean_collab_columns()
        self.__clean_keywords_columns()

    def __clean_department(self):
        self.df['department'] = self.df['department'].replace('clinical and health psychology', 'Clinical and Health Psychology')

        avoid_prefixing = ['Department of ', 'Dept. of ', 'Institute', 'Ludwig', 'Outpatient', 'Before:']
        self.df['department'] = self.df['department'].apply(lambda x: x if any(x.startswith(prefix) for prefix in avoid_prefixing) else 'Department of ' + x)

        self.df['department'] = self.df['department'].replace('Before: Department of Clinical and Health Psychology, but recently moved to MedUni Wien', 'Department of Clinical and Health Psychology')
        self.df['department'] = self.df['department'].replace('Department of Cognition, Emotion, and Methods', 'Department of Cognition, Emotion, and Methods in Psychology')
        self.df['department'] = self.df['department'].replace('Dept. of Social and Cultural Anthropology', 'Department of Social and Cultural Anthropology')
        self.df['department'] = self.df['department'].replace('Department of Science & Technology Studies ; Sociology (double affiliation, starting Mach 1) ', 'Department of Sociology')

    def __clean_collab_columns(self):
        df_collab_fac_split = self.df['collab_faculties'].str.split('+', expand=True)
        df_collab_fac_split.columns = ['collab_fac1', 'collab_fac2']
        df_collab_fac_split.replace(['-99', float('nan')], None, inplace=True)
        self.df = pd.concat([self.df.drop(columns=['collab_faculties']), df_collab_fac_split], axis=1)

        df_collab_uni_split = self.df['collab_unis'].str.split('+', expand=True)
        df_collab_uni_split.columns = ['collab_uni1', 'collab_uni2', 'collab_uni3', 'collab_uni4']
        df_collab_uni_split.replace(['-99', float('nan')], None, inplace=True)
        self.df = pd.concat([self.df.drop(columns=['collab_unis']), df_collab_uni_split], axis=1)

    def __clean_keywords_columns(self):
        keyword_columns = ['health_research_keywords', 'research_methods_keywords']
        COMMA_AND_SEMICOLON = r'[;,]'

        for keyword_column in keyword_columns:
            self.df[keyword_column] = self.df[keyword_column].str.split(COMMA_AND_SEMICOLON, expand=False)
            self.df[keyword_column] = self.df[keyword_column].apply(lambda x: [keyword.strip() for keyword in x if keyword.strip()])


