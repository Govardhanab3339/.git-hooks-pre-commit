import os
import sys
import polars as pl

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class nearestOptions():
    
    def __init__(self, Symbol, Instrument, exch='NFO'):
        self.exch = exch
        self.Symbol = Symbol
        self.Instrument = Instrument
    
    def __get_Sorted_options(self):        
        symbol_df = pl.read_csv(f'https://api.shoonya.com/{self.exch}_symbols.txt.zip')
        symbol_df = symbol_df.with_column(pl.col('Expiry').str.strptime(pl.Date, '%Y-%m-%d'))
        
        if self.Instrument == 'INDEX' and self.Symbol == 'Nifty 50':
            self.Symbol = "NIFTY"
        elif self.Instrument == 'INDEX' and self.Symbol == 'Nifty Bank':
            self.Symbol = "BANKNIFTY"
        elif self.Instrument == 'INDEX' and self.Symbol == 'Nifty Fin Services':
            self.Symbol = "FINNIFTY"
        elif self.Instrument == 'INDEX' and self.Symbol == 'NIFTY MID SELECT':
            self.Symbol = "MIDCPNIFTY"
        
        opt_SortedByExpiry_symbol_df = symbol_df.filter(pl.col('Symbol') == self.Symbol)
        return opt_SortedByExpiry_symbol_df

    def Sorted_CE_PE_Options(self):
        opt_SortedByExpiry_symbol_df = self.__get_Sorted_options()
        opt_SortedByExpiry_symbol_ce = opt_SortedByExpiry_symbol_df.filter(pl.col('OptionType') == 'CE')
        opt_SortedByExpiry_symbol_pe = opt_SortedByExpiry_symbol_df.filter(pl.col('OptionType') == 'PE')
        return opt_SortedByExpiry_symbol_ce, opt_SortedByExpiry_symbol_pe

# Example usage:
# obj_opt_Sorted_Nifty_CE_PE = nearestOptions(Symbol='NIFTY', Instrument='INDEX')
# print(obj_opt_Sorted_Nifty_CE_PE.Sorted_CE_PE_Options())

# obj_opt_Sorted_BankNifty_CE_PE = nearestOptions(Symbol='BANKNIFTY', Instrument='INDEX')
# print(obj_opt_Sorted_BankNifty_CE_PE.Sorted_CE_PE_Options())
