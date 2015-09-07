import psycopg2

from xetracker.model import currency_conversion

class CurrencyConversionDAO:
  def __init__(self):
    self.connection = psycopg2.connect("dbname = 'xe' user = 'timofeya' host = 'localhost'")

  def upsert(self, currency_conversions):
    cursor = self.connection.cursor()
    for currency_conversion in currency_conversions:
      cursor.execute("""
          INSERT INTO xetracker.currency_conversion (cc_provider, cc_currency_from, cc_currency_to, cc_provider_selling_rate, cc_provider_buying_rate, cc_conversion_time)
          SELECT %s, %s, %s, %s, %s, %s
           WHERE NOT EXISTS (
                SELECT 1
                  FROM xetracker.currency_conversion
                 WHERE cc_provider = %s
                   AND cc_currency_from = %s
                   AND cc_currency_to = %s
                   AND cc_conversion_time = %s
              )
        """, (
              # SELECT CLAUSE
                currency_conversion.provider,
                currency_conversion.currency_from,
                currency_conversion.currency_to,
                currency_conversion.provider_selling_rate,
                currency_conversion.provider_buying_rate,
                currency_conversion.conversion_time,
            # NOT EXISTS CLAUSE
                currency_conversion.provider,
                currency_conversion.currency_from,
                currency_conversion.currency_to,
                currency_conversion.conversion_time
             ))
    
    cursor.close()
    self.connection.commit()

  def get(self, provider, currency_from, currency_to, conversion_time):
    cursor = self.connection.cursor()
    cursor.execute("""
      SELECT cc_provider, cc_currency_from, cc_currency_to, cc_provider_selling_rate, cc_provider_buying_rate, cc_conversion_time
        FROM xetracker.currency_conversion
       WHERE cc_provider = %s
         AND cc_currency_from = %s
         AND cc_currency_to = %s
         AND cc_conversion_time = %s
    """, (provider, currency_from, currency_to, conversion_time))

    row = cursor.fetchone()

    cursor.close()
    self.connection.commit()

    return currency_conversion.CurrencyConversion(row[0], row[1], row[2], row[3], row[4], row[5]) if row is not None else None 
