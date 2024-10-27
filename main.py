# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
# from src.data_extraction import extract_telegram_data, extract_twitter_data
# from src.sentiment_analysis import analyze_sentiment
# from src.data_categorization import categorize_data
# from src.insights_generation import generate_insights
# from src.visualization import plot_sentiment_for_each_company

# # Function to save DataFrame as CSV, Excel, and PDF
# def save_dataframe(df, filename_base):
#     try:
#         # Save as CSV
#         csv_file = f"{filename_base}.csv"
#         df.to_csv(csv_file, index=False)
#         print(f"Data saved as CSV: {csv_file}")

#         # Save as Excel
#         excel_file = f"{filename_base}.xlsx"
#         df.to_excel(excel_file, index=False)
#         print(f"Data saved as Excel: {excel_file}")

#         # Save as PDF
#         pdf_file = f"{filename_base}.pdf"
#         with PdfPages(pdf_file) as pdf:
#             fig, ax = plt.subplots(figsize=(10, len(df) * 0.5))  # Adjust size based on number of rows
#             ax.axis('tight')
#             ax.axis('off')
#             table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
#             table.auto_set_font_size(False)
#             table.set_fontsize(10)
#             table.scale(1.2, 1.2)
#             pdf.savefig(fig, bbox_inches='tight')
#             plt.close(fig)
#         print(f"Data saved as PDF: {pdf_file}")

#     except Exception as e:
#         print(f"Error while saving data: {e}")
# def main():
#     try:
#         print("Loading company data...")
#         # Load company data from ind_nifty500list.csv
#         company_data_path = os.path.join('data', 'ind_nifty50list.csv')
#         companies_df = pd.read_csv(company_data_path)
#         print("Company data loaded successfully.")
        
#         companies_df = companies_df[['Company Name', 'Symbol']]
#         companies_df.columns = ['company_name', 'symbol']
        
#         print("============ Data Extraction and Sentiment Analysis ============")
#         all_company_sentiment_results = []

#         # Loop through each company in the NSE 500 list
#         for index, row in companies_df.iterrows():
#             company_name = row['company_name']
#             symbol = row['symbol']
#             print(f"Processing data for company: {company_name} ({symbol})")
#             print(pd.DataFrame([row]))

#             # Extract Telegram data
#             extracted_data = extract_telegram_data()
#             if extracted_data is None or extracted_data.empty:
#                 print(f"No data extracted for {company_name}. Skipping...")
#                 continue
#             print(f"Extracted data for {company_name}: \n{extracted_data}")

#              # Rename 'content' to 'message' to make it compatible with sentiment analysis
#             if 'content' in extracted_data.columns:
#                 extracted_data.rename(columns={'content': 'message'}, inplace=True)
#                 print("'content' column renamed to 'message'.")

#             # Check if the 'message' column is present
#             if 'message' not in extracted_data.columns:
#                 print(f"Data for {company_name} does not contain a 'message' column. Skipping sentiment analysis...")
#                 continue

#                     # Create a folder for saving extracted data
#             folder_name = 'extracted_data_500_Nse_company'
#             if not os.path.exists(folder_name):
#                 os.makedirs(folder_name)
#                 print(f"Folder '{folder_name}' created.")

#             # Save the extracted data to a CSV file in the folder
#             extracted_data_filename = os.path.join(folder_name, f"{company_name}_raw_extracted_telegram_data.csv")
#             extracted_data.to_csv(extracted_data_filename, index=False)
#             print(f"Extracted data saved to '{extracted_data_filename}'.")

#             # Perform sentiment analysis
#             print(f"Performing sentiment analysis for {company_name}...")
#             sentiment_results = analyze_sentiment(extracted_data)
#             if sentiment_results is None or sentiment_results.empty:
#                 print(f"No sentiment results for {company_name}. Skipping...")
#                 continue
#             print(f"Sentiment analysis for {company_name}: \n{sentiment_results.head()}")

#             # Save sentiment results to the same folder
#             sentiment_results_filename = os.path.join(folder_name, f"{company_name}_sentiment_results.csv")
#             sentiment_results.to_csv(sentiment_results_filename, index=False)
#             print(f"Sentiment results saved to '{sentiment_results_filename}'.")

#             # Append results to all_company_sentiment_results
#             sentiment_results['company_name'] = company_name
#             all_company_sentiment_results.append(sentiment_results)

#         # Concatenate all sentiment results
#         if all_company_sentiment_results:
#             all_sentiment_df = pd.concat(all_company_sentiment_results, ignore_index=True)
#             save_dataframe(all_sentiment_df, os.path.join(folder_name, 'nse500_sentiment_analysis'))

#             print("Sentiment analysis and insights generation completed successfully.")
#         else:
#             print("No sentiment results to process.")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()
import os
import pandas as pd
import matplotlib.pyplot as plt
from src.data_extraction import extract_telegram_data
from src.sentiment_analysis import analyze_sentiment
from matplotlib.backends.backend_pdf import PdfPages

def calculate_relative_strength(stock_data, benchmark_data):
    rs = stock_data / benchmark_data
    rs_momentum = rs.pct_change(fill_method=None)
    print(rs,calculate_relative_strength,"strength")
    print(pd.DataFrame({'RS': rs, 'RS_Momentum': rs_momentum}))
    return pd.DataFrame({'RS': rs, 'RS_Momentum': rs_momentum})

def classify_rrg_quadrant(rs, rm):
    try:
        rs, rm = float(rs), float(rm)
        if rs > 100 and rm > 0: return 'Leading'
        elif rs > 100 and rm < 0: return 'Weakening'
        elif rs < 100 and rm < 0: return 'Lagging'
        else: return 'Improving'
    except ValueError:
        return 'Unknown'

def plot_rrg(data, filename):
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = {'Leading': 'green', 'Weakening': 'yellow', 'Lagging': 'red', 'Improving': 'blue'}
    for _, row in data.iterrows():
        color = colors.get(row['Quadrant'], 'black')
        ax.scatter(row['RS'], row['RS_Momentum'], c=color, label=row['symbol'])
        ax.text(row['RS'], row['RS_Momentum'], row['symbol'], fontsize=9)
    ax.axhline(0, color='black')
    ax.axvline(100, color='black')
    plt.title('Relative Rotation Graph (RRG)')
    plt.xlabel('Relative Strength (RS)')
    plt.ylabel('Relative Momentum (RM)')
    plt.grid(True)
    plt.savefig(filename)
    plt.close(fig)

def save_dataframe(df, filename_base):
    try:
        df.to_csv(f"{filename_base}.csv", index=False)
        df.to_excel(f"{filename_base}.xlsx", index=False)
        with PdfPages(f"{filename_base}.pdf") as pdf:
            fig, ax = plt.subplots(figsize=(10, len(df) * 0.5))
            ax.axis('tight')
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.2)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    try:
        folder_name = 'extracted_data_500_Nse_company'
        os.makedirs(folder_name, exist_ok=True)
        data_path = 'data/Updated Nifty 50 Historical DataSet with Tiker (Symbol)'
        company_list_path = os.path.join('data', 'ind_nifty50list.csv')
        companies_df = pd.read_csv(company_list_path)
        companies_df = companies_df[['Company Name', 'Symbol']].rename(columns={'Company Name': 'company_name', 'Symbol': 'symbol'})

        rrg_results = []
        all_company_sentiment_results = []

        for _, row in companies_df.iterrows():
            company_name, symbol = row['company_name'], row['symbol']
            stock_file_path = os.path.join(data_path, f"{symbol} Historical Data.csv")
            
            if not os.path.exists(stock_file_path):
                print(f"Stock data not available for {symbol}. Skipping RRG analysis...")
                continue
            
            stock_data = pd.read_csv(stock_file_path, parse_dates=['Date'], dayfirst=True)
            stock_data.rename(columns={'Date': 'Month', 'Price': 'Close Price'}, inplace=True)
            stock_data['Close Price'] = pd.to_numeric(stock_data['Close Price'], errors='coerce').dropna()

            benchmark_data = stock_data['Close Price'].copy()

            extracted_data = extract_telegram_data()
            if extracted_data is None or extracted_data.empty:
                continue
            extracted_data.rename(columns={'content': 'message'}, inplace=True)
            sentiment_results = analyze_sentiment(extracted_data)
            if sentiment_results.empty:
                continue
            
                     #Create a folder for saving extracted data
            folder_name = 'extracted_data_500_Nse_company'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                print(f"Folder '{folder_name}' created.")

            # Save the extracted data to a CSV file in the folder
            extracted_data_filename = os.path.join(folder_name, f"{company_name}_raw_extracted_telegram_data_substances.csv")
            extracted_data.to_csv(extracted_data_filename, index=False)
            print(f"Extracted data saved to '{extracted_data_filename}'.")

            
            sentiment_results['company_name'] = company_name
            all_company_sentiment_results.append(sentiment_results)
            save_dataframe(sentiment_results, os.path.join(folder_name, f"{company_name}_sentiment_results"))
            
            rs_rm = calculate_relative_strength(stock_data['Close Price'], benchmark_data)
            latest_rs, latest_rm = rs_rm['RS'].iloc[-1], rs_rm['RS_Momentum'].iloc[-1]
            quadrant = classify_rrg_quadrant(latest_rs, latest_rm)
            
            rrg_results.append({
                'company_name': company_name,
                'symbol': symbol,
                'RS': latest_rs,
                'RS_Momentum': latest_rm,
                'Quadrant': quadrant
            })

            if rrg_results:
                rrg_df = pd.DataFrame(rrg_results)
                save_dataframe(rrg_df, os.path.join(folder_name, f"{company_name}_nse500_rrg_results"))
                plot_rrg(rrg_df, os.path.join(folder_name, f"{company_name}_nse500_rrg_chart.pdf"))
                print("RRG analysis and plotting completed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
