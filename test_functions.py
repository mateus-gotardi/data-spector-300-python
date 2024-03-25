import unittest
from functions import processar_linha, get_next_month, get_prev_month, calc_totalPeriod, calc_data, fix_next_cicle_date, make_yy_mm

class TestFunctions(unittest.TestCase):
    def test_processar_linha(self):
        linha = '1,30,5/2/22 23:25,Atrasada,5/12/22 07:31,,"23,81",09/05/2023,user_2779'
        coluna = processar_linha(linha)
        self.assertEqual(coluna, ['1', '30', '5/2/22 23:25','Atrasada', '5/12/22 07:31','','"23,81"','09/05/2023','user_2779'])

    def test_make_yy_mm(self):
        date = '5/2/22 23:25'
        formatted = make_yy_mm(date)
        self.assertEqual(formatted, '22-05')

    def test_get_next_month (self):
        date = '22-05'
        last_month = '22-12'
        self.assertEqual(get_next_month(date), '22-06')
        self.assertEqual(get_next_month(last_month), '23-01' )
    
    def test_get_prev_month (self):
        date = '22-05'
        first_month = '23-01'
        self.assertEqual(get_prev_month(date), '22-04')
        self.assertEqual(get_prev_month(first_month), '22-12' )

    def test_fix_next_cicle_date (self):
        self.assertEqual(fix_next_cicle_date('09/05/2023'), '23-05')
        self.assertEqual(fix_next_cicle_date('12/17/2024'), '24-12')


    def test_calc_totalPeriod(self):
        data = [['1', '30', '5/2/22 23:25','Ativa', '5/12/22 07:31','','"23,81"','09/05/2023','user_2779'], 
                ['1', '30', '2/18/24 23:25','Ativa', '9/19/22 07:31','','"23,81"','19/02/2024','user_279']]
        period = calc_totalPeriod(data)
        self.assertEqual(period.get('keys'), ['22-05', '22-06', '22-07', '22-08', '22-09', '22-10', '22-11', '22-12', '23-01', '23-02', '23-03', '23-04', '23-05', '23-06', '23-07','23-08', '23-09', '23-10', '23-11', '23-12', '24-01', '24-02'])
        self.assertEqual(period.get('years'), ['22', '23', '24'])

    def test_calc_data(self):
        csv_mock = [
            # [quantidade cobranças, cobrada a cada X dias, data início, status, data status, data cancelamento, valor, próximo ciclo, ID assinante]
            ['1', '30', "2/6/22 17:48", 'Cancelada', "3/15/22 9:44", "3/15/22 9:44", '"131.4"', "3/3/2022", 'user_1001'],
            ['1', '30', "3/10/22 10:30", 'Ativa', "3/15/22 9:44", '', '"200.0"', "3/10/2023", 'user_200'],
            ['1', '30', "3/8/22 23:17", 'Cancelada', "6/14/22 9:36", "5/14/22 9:36", '"367.6"', "6/4/2022", 'user_100'],
            ['1', '30', "4/10/22 10:30", 'Ativa', "3/15/22 9:44", '', '"204.0"', "3/10/2023", 'user_230'],
            ['1', '30', "5/10/22 10:30", 'Ativa', "3/15/22 9:44", '', '"240.0"', "3/10/2023", 'user_208'],
        ]
        data = calc_data(csv_mock)
        print(data)
        self.assertEqual(data.get('monthly').get('mrr'), {'22-02': 131.4, '22-03': 699, '22-04': 771.6, '22-05': 644})
        self.assertEqual(data.get('monthly').get('churn_rate'), {'22-02': 0.0, '22-03': 100, '22-04': 0.0, '22-05': 33.33})
if __name__ == '__main__':
    unittest.main()
