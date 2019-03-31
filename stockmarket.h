#ifndef STOCKMARKET_H
#define STOCKMARKET_H

#include <QMainWindow>
#include<QObject>
#include<QTableWidget>
#include<fstream>
#include<string>
#include<QString>




namespace Ui {
class StockMarket;
}

class StockMarket : public QMainWindow
{
    Q_OBJECT

public:

    explicit StockMarket(QWidget *parent = nullptr);
    ~StockMarket();

public slots:
    void changeparameter();




private:
    Ui::StockMarket *ui;


    std::string company;
   std::string time;
    std::string parameter;

};

#endif // STOCKMARKET_H
