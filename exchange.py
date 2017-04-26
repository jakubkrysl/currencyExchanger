#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import json
import forex_python
from forex_python.converter import CurrencyRates
from exceptions import NotImplementedError
import sys
import os

# USAGE EXAMPLE:     
# python RocketMap\_git\currencyExchanger\exchange.py --amount 100 --input_currency EUR --output_currency CZK

class Exchange(object):
    def __init__(self, amount, input, output):
        
        with open(os.path.dirname(os.path.abspath(forex_python.__file__)) + '/raw_data/currencies.json', 'r') as f:
            self.currencies = json.loads(f.read())
            
        self.amount = amount
        if self.amount is None:
            print("Error: argument --amount is required.")
            sys.exit(1)
            
        self.input = input
        if self.input is None:
            print("Error: argument --input_currency is required.")
            sys.exit(1)
            
        self.output = output
        self.converter = CurrencyRates()
    
    def checkCurrencyCode(self, code):
        for x in self.currencies:
            if(x['cc'] == code):
                return True
        return False
                    
    def switchSymbolToCurrencyCode(self, symbol):
        code = []
        for x in self.currencies:
            for i in (x['symbol']).encode('utf-8'):
                if(i == symbol):
                    code.append(x)     
        return code
    
    def askCurrencyCode(self, symbol):
        output_list = self.switchSymbolToCurrencyCode(symbol)
        print("Found more currencies under this symbol.")
        for i,x in enumerate(output_list):
            print("{}: code = {}, name = {}".format(i, str(x['cc'].encode('utf-8')), str(x['name'].encode('utf-8'))))
            x['id'] = i
        vstup = len(output_list)+1
        while(vstup >= len(output_list) or vstup < 0):
            try:
                vstup = int(input("Which one did you mean? (type number)  "))
                if(vstup >= len(output_list) or vstup < 0):
                    print("The number must be inside 0 and {} range".format(len(output_list)-1))
            except NameError:
                print("Must be a number")
            except KeyboardInterrupt:
                print("Interrupted by keyboard, exiting")
                sys.exit(1) 
            except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)
        for key in output_list:
            if key['id'] == vstup:
                return str(key['cc'])
    
    def exchange(self, amount, input, output):
        if(not self.output):
            self.to_all = True
            print("Converting to all currencies.")
            raise NotImplementedError, "Not implemented yet!"
        else:            
            return self.converter.convert(input, output, amount)
    
    def fillJson(self):
        try:
            self.data = {
                "input": { 
                    "amount": "{0:.2f}".format(self.amount),
                    "currency": self.input
                },
                "output": {
                }
            }
            if(self.checkCurrencyCode(self.input)):
                self.data['input']['currency'] = self.input
            else:
                self.input =self.askCurrencyCode(self.input)
                self.data['input']['currency'] = self.input
                
            if(self.checkCurrencyCode(self.output)):
                print("Converting to specified currency.")
                self.data['output'][self.output] = "{0:.2f}".format(self.exchange(self.amount, self.input, self.output)) 
            else:
                self.output = self.askCurrencyCode(self.output)
                self.data['output'][self.output] = "{0:.2f}".format(self.exchange(self.amount, self.input, self.output))

        except NotImplementedError:
            print("Error: Not implemented yet!")
            sys.exit(1)   
        except KeyError:
            print("Error: used unknown currency")
            sys.exit(1)    
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)
            sys.exit(1)           
        return self.data
                

if __name__ == "__main__":    
    
    parser = argparse.ArgumentParser(description="This is a currency echanger.")
    
    parser.add_argument("--amount", type=float, help="amount which we want to convert")
    parser.add_argument("--input_currency", type=str, help="input currency - 3 letters name or currency symbol")     
    parser.add_argument("--output_currency", type=str, help="requested/output currency - 3 letters name or currency symbol")   
    args = parser.parse_args()

    converter = Exchange(args.amount, args.input_currency, args.output_currency)
    data = converter.fillJson()
    print(data)      
        
    with open('exchanged.json', 'w') as outfile:
        json.dump(data, outfile)

