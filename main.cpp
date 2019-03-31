#include "stockmarket.h"
#include <QApplication>
#include<Python/Python.h>
#include<unistd.h>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    StockMarket w;



    w.show();

    return a.exec();
}
