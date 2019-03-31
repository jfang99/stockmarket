#include "stockmarket.h"
#include "ui_stockmarket.h"
#include<QTableWidget>
#include<QProcess>
#include"QDebug"
#include<QtGui>

StockMarket::StockMarket(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::StockMarket)
{

    ui->setupUi(this);
    setWindowTitle("Prediction on Historical Performance Data");
    setStyleSheet("QMainWindow {background: 'darkBlue';}");
   /* this->setStyleSheet(
                "#centralWidget { "
                " border-image: url(:/new/prefix1/images.jpeg) 0 0 0 0 stretch stretch;"
                "}");*/
QObject::connect(ui->submit,SIGNAL(clicked()),this,SLOT(changeparameter()));


}


void StockMarket::changeparameter(){
    company=(ui->company->toPlainText()).toStdString();
    //time=(ui->time->text()).toStdString();
    //parameter=(ui->combobox->text()).toStdString();
    std::string str= "/Users/mac/Desktop/StockMarket/Header.py";

    QStringList arguments;
    arguments  << "/Users/mac/Desktop/StockMarket/Header.py" << QString::fromStdString(company) ;

    QProcess p;



    p.start("python",arguments);
    //p.start("python",arguments);
    p.waitForFinished();

    qDebug() << p.readAllStandardError();
    QString p_stdout;
    p_stdout = p.readAllStandardOutput();
    qDebug() << p_stdout;

    ui->price->setPlainText(p_stdout);

    QPixmap stat_GO ("/Users/mac/Desktop/StockMarket/images.jpeg");
        ui->graph->setPixmap(stat_GO);
    return;
}

StockMarket::~StockMarket()
{
    delete ui;
}
