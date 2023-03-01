import pandas as pd


def get_pandas_frame_of_input():
    # returns contents of an input.txt file as pandas DataFrame
    filename = 'input.txt'
    while filename.lower() != 'q': 
        try:
            frame = pd.read_csv(filename, header=None)
            frame[1] = pd.to_datetime(frame[1])
            frame[2] = pd.to_datetime(frame[2])
            frame = frame.rename(columns={0: 'policyNumber', 1: 'startDate', 2: 'endDate', 3: 'premiumAmount'})
            return frame
        except FileNotFoundError:
            print('Unable to identify input file: ' + filename)
            print('Please enter the name of the input file or \'q\' to quit')
            filename = input('-> ')
        except Exception:
            raise Exception('Something went wrong reading from input file.')


def analyze_policy(policyNumber, startDate, endDate, premiumAmount):
    # calculates the monthly premiums for a policy, returned as a pandas DataFrame
    premium_per_day = premiumAmount / (endDate - startDate).days
    data_dict = []

    current_date = startDate
    while True:
        nextDate = current_date + pd.offsets.MonthEnd() + pd.Timedelta(1, 'd')
        if (nextDate >= endDate):
            nextDate = endDate
            amount_earned = (nextDate - current_date).days * premium_per_day
            data_dict.append({
                'policyNumber': policyNumber, 
                'monthEarned': current_date.to_period('M'), 
                'amountEarned': round(amount_earned, 2)})
            break
        else:
            amount_earned = (nextDate - current_date).days * premium_per_day
            data_dict.append({
                'policyNumber': policyNumber, 
                'monthEarned': current_date.to_period('M'), 
                'amountEarned': round(amount_earned, 2)})
        current_date = nextDate

    new_frame = pd.DataFrame(data_dict)
    return new_frame


def analyze_all_policies(input_df, output_file):
    # outputs the monthly premiums for all policies in input.txt to a csv file
    frames = []
    for index, row in input_df.iterrows():
        analysis = analyze_policy(
            row['policyNumber'], 
            row['startDate'], 
            row['endDate'], 
            row['premiumAmount'])
        frames.append(analysis)
    combined_frames = pd.concat(frames)
    combined_frames.to_csv(output_file, index=False)
    print('The calculated monthly premiums have been outputted to: ' + output_file)

if (__name__ == '__main__'):
    frame = get_pandas_frame_of_input()
    analyze_all_policies(frame, 'output.csv')
    
