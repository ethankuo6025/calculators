CONTRIBUTION = 7500
INFLATION = .03
STARTING_VALUE = 60000
EV_PERCENT = .1
YEARS = 43
price_index = 1

for i in range(0, YEARS):
    CONTRIBUTION *= (1+INFLATION)
    change = CONTRIBUTION - CONTRIBUTION%500 
    STARTING_VALUE += change
    STARTING_VALUE *= (1+EV_PERCENT)
    price_index *= (1 + INFLATION)  
    print(f"year {2026+i} nominal: {STARTING_VALUE:>15,.2f}  real: {STARTING_VALUE/price_index:>15,.2f}")