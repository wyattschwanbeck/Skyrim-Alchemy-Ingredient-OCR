# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 11:37:55 2021

@author: wyatt
"""
import pandas as pd



class IngredientManager():
	def __init__(self):
		self.IngList = pd.read_csv("Alchemy-Effects.csv")
		self.UnknownEffects = pd.DataFrame(columns = ["Name", \
												"UnknownFirst", \
												"UnknownSecond", \
												"UnknownThird", \
												"UnknownFourth", \
												"All Ingredients"])

	def AddPlayerIng(self, IngName, KnownFirst, KnownSecond, KnownThird, KnownFourth):
		#From Ingredient list grab DF

		#Remove occurances where there are multiple ingredients to only capture ingredient name
		if " (" in IngName:
			IngName = IngName[0:IngName.find('(')].lstrip().rstrip()
		else:
			IngName = IngName.lstrip().rstrip()
		print("Parsing for " + IngName)
		temp_df = self.IngList.loc[self.IngList['Name'].str.contains(IngName)]
		if len(temp_df) ==0:
			#Do extra parsing testing each letter as a wild card that could match
			# WILL ONLY WORK IF ONE CHAR WAS READ ERRONEOUSLY BY OCR
			# In REGEX format, check every single letter in read ingredient and replace it with wildcard
			for i in range(0,len(IngName)):
				if i < len(IngName):
					IngCharFirst = "^" + IngName[0:i]
					IngCharLast = IngName[i+1:len(IngName)]+"$"
					IngLookup = IngCharFirst + r".*" + IngCharLast
				else:
					#To prevent indexing errors, update string to check last letter
					IngLookup = "^" + IngName[0:-1] + r".*$"

				temp_df = self.IngList.loc[self.IngList['Name'].str.contains(IngLookup, regex=True)]
				if len(temp_df) > 0:
					break

		#Check if IngName was found. Check if ingredients are known.
		# Print failure notification of what was parsed if not
		if len(temp_df)>0:
			if KnownFirst == False:
				UnknownFirst = temp_df.values[0][2]
			else: UnknownFirst=temp_df.values[0][2] + " (Known)"
			if KnownSecond == False:
				UnknownSecond = temp_df.values[0][3]
			else: UnknownSecond= temp_df.values[0][3]+" (Known)"
			if KnownThird == False:
				UnknownThird = temp_df.values[0][4]
			else: UnknownThird=temp_df.values[0][4] + " (Known)"
			if KnownFourth == False:
				UnknownFourth = temp_df.values[0][5]
			else: UnknownFourth= temp_df.values[0][5] + " (Known)"
			All_Ingredients = UnknownFirst + ", " + \
				UnknownSecond + ", "  + \
				UnknownThird + ", " + \
				UnknownFourth
			self.UnknownEffects = self.UnknownEffects.append({"Name":temp_df.values[0][0], \
													 "UnknownFirst": UnknownFirst, \
													 "UnknownSecond": UnknownSecond, \
													 "UnknownThird":UnknownThird, \
													 "UnknownFourth":UnknownFourth, \
													 "All Ingredients" : All_Ingredients}, \
													ignore_index=True)
		else:
			print(IngName + " was not found in total ingredient list.")

	def ExportToCSV(self):
		self.UnknownEffects.to_csv("Parsed_Character_Ingredients.csv")


