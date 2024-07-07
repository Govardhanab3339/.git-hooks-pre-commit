import os
import sys
import polars as pl

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Symbols_Idx_Fut():
    exch = Symbol = Instrument = ''
    
    def __init__(self, exch, Symbol, Instrument):
        self.exch = exch
        self.Symbol = Symbol
        self.Instrument = Instrument

    def get_NSE_IDX_NFO_FUT(self):      
        symbol_df = pl.read_csv(f'https://api.shoonya.com/{self.exch}_symbols.txt.zip')
        Symbol_boolean_mask = (symbol_df['Symbol'] == self.Symbol) & (symbol_df['Instrument'] == self.Instrument)
        filtered_symbol_df = symbol_df.filter(Symbol_boolean_mask)
        
        if self.Instrument == 'FUTIDX':
            filtered_symbol_df = filtered_symbol_df.with_column(pl.col('Expiry').str.strptime(pl.Date, '%d-%b-%Y'))
            Sorted_filtered_symbol_df = filtered_symbol_df.sort('Expiry')
            Symbol_tkn_series = Sorted_filtered_symbol_df['Token']
            Symbol_TradingSymbol_series = Sorted_filtered_symbol_df['TradingSymbol']
        else:
            Symbol_tkn_series = filtered_symbol_df['Token']
            Symbol_TradingSymbol_series = filtered_symbol_df['TradingSymbol']

        Symbol_tkn = Symbol_tkn_series[0]
        Symbol_TradingSymbol = Symbol_TradingSymbol_series[0]

        del Symbol_tkn_series, Symbol_TradingSymbol_series, filtered_symbol_df, Symbol_boolean_mask, symbol_df
            
        return (Symbol_tkn, Symbol_TradingSymbol)

# Example usage:
# obj_idx_nifty50 = Symbols_Idx_Fut(exch='NSE', Symbol='Nifty 50', Instrument='INDEX') 
# print(obj_idx_nifty50.get_NSE_IDX_NFO_FUT())

# obj_futx_nifty = Symbols_Idx_Fut(exch='NFO', Symbol='NIFTY', Instrument='FUTIDX') 
# print(obj_futx_nifty.get_NSE_IDX_NFO_FUT())

# obj_idx_niftybank = Symbols_Idx_Fut(exch='NSE', Symbol='Nifty Bank', Instrument='INDEX') 
# print(obj_idx_niftybank.get_NSE_IDX_NFO_FUT())

# obj_futx_niftybank = Symbols_Idx_Fut(exch='NFO', Symbol='BANKNIFTY', Instrument='FUTIDX') 
# print(obj_futx_niftybank.get_NSE_IDX_NFO_FUT())
