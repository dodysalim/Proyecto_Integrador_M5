from build_powerbi import *
from build_powerbi import PROJECT_ROOT
import sys, ast, numpy as np
from sklearn.model_selection import train_test_split
from scipy.stats import ks_2samp, chi2_contingency

def m5():
 repo='Proyecto_Integrador_M5';r=Report(repo,'Monitor MLOps M5','10.763 registros · Referencia/Actual son particiones 80/20 del dataset, no datos de producción')
 d=pd.read_excel(PROJECT_ROOT/'Base_de_datos.xlsx').drop(columns=['puntaje']);a,b=train_test_split(d,test_size=.2,random_state=42,stratify=d.Pago_atiempo);a=a.copy();b=b.copy();a['Dataset']='Referencia';b['Dataset']='Actual';all=pd.concat([a,b]);all=all.drop(columns=['fecha_prestamo']);all['GrupoEdad']=(all.edad_cliente//10*10).astype(str)
 r.table('Creditos',all,metrics('Creditos',[('Registros','COUNTROWS(Creditos)'),('Capital','SUM(Creditos[capital_prestado])'),('Mora','SUM(Creditos[saldo_mora])'),('Edad','AVERAGE(Creditos[edad_cliente])')]))
 numerical=[];categorical=[];distribution=[];correlation=[]
 for col in d.select_dtypes(include='number'):
  if col=='Pago_atiempo':continue
  x=a[col].dropna();y=b[col].dropna();ks,p=ks_2samp(x,y);bins=np.unique(np.quantile(x,np.linspace(0,1,11)));bins[0]=-np.inf;bins[-1]=np.inf
  xc=np.histogram(x,bins=bins)[0];yc=np.histogram(y,bins=bins)[0];xr=(xc+1e-6)/len(x);yr=(yc+1e-6)/len(y);psi=float(np.sum((xr-yr)*np.log(xr/yr)));numerical.append([col,ks,p,psi,int(p<.001 or psi>.2)])
  for label,data in [('Referencia',x),('Actual',y)]:
   edges=np.linspace(min(x.min(),y.min()),max(x.max(),y.max())+.000001,21);counts,_=np.histogram(data,bins=edges)
   for i,count in enumerate(counts):distribution.append([col,label,float((edges[i]+edges[i+1])/2),int(count),float(count/len(data))])
 for col in d.select_dtypes(exclude=['number','datetime']):
  if col=='fecha_prestamo':continue
  cross=pd.concat([a[col].value_counts(),b[col].value_counts()],axis=1).fillna(0);stat,p,_,_=chi2_contingency(cross.values.T);categorical.append([col,stat,p,int(p<.001)])
 for label,data in [('Referencia',a),('Actual',b)]:
  corr=data.select_dtypes(include='number').corr()
  for c in corr:
   for c2 in corr:correlation.append([label,c,c2,corr.loc[c,c2]])
 r.table('DriftNumerico',pd.DataFrame(numerical,columns=['Variable','KS','PValue','PSI','Alerta']),metrics('DriftNumerico',[('PSI','MAX(DriftNumerico[PSI])'),('KS','MAX(DriftNumerico[KS])'),('Alertas','SUM(DriftNumerico[Alerta])')]))
 r.table('DriftCategorico',pd.DataFrame(categorical,columns=['Variable','Chi2','PValue','Alerta']),metrics('DriftCategorico',[('Chi2','MAX(DriftCategorico[Chi2])')]))
 r.table('Distribuciones',pd.DataFrame(distribution,columns=['Variable','Dataset','Intervalo','Conteo','Proporcion']),metrics('Distribuciones',[('Proporcion','SUM(Distribuciones[Proporcion])')]))
 r.table('Correlaciones',pd.DataFrame(correlation,columns=['Dataset','Variable','Variable2','Correlacion']),metrics('Correlaciones',[('Correlacion','MAX(Correlaciones[Correlacion])')]))
 filters=[('Creditos','Dataset'),('Creditos','tipo_laboral'),('Creditos','GrupoEdad')]
 r.page('salud','01 · Estado de salud y target drift',filters);r.cards('Creditos',list(r.measures['Creditos']));r.chart('Creditos','Pago_atiempo','KPI_Registros','Distribución del target · por partición',30,270,kind='column',legend='Dataset');r.chart('Creditos','tendencia_ingresos','KPI_Registros','Tendencia de ingresos',650,270,legend='Dataset');r.tablevisual('DriftNumerico',['Variable','KS','PValue','PSI','Alerta'],'Diagnóstico de drift · umbrales p < 0,001 y PSI > 0,2',30,570,1220,260)
 r.page('numerico','02 · Drift numérico',[('DriftNumerico','Variable')],note='Estadísticas precalculadas para el split completo. Los filtros de clientes de otras páginas no recalculan KS/PSI.')
 r.chart('DriftNumerico','Variable','KPI_PSI','Population Stability Index',30,160);r.chart('DriftNumerico','Variable','KPI_KS','Estadístico Kolmogorov-Smirnov',650,160);r.tablevisual('DriftNumerico',list(r.tables['DriftNumerico']),'P-valores y alertas',30,470,1220,360)
 r.page('categorico','03 · Drift categórico',[('DriftCategorico','Variable')]);r.chart('DriftCategorico','Variable','KPI_Chi2','Chi-cuadrado · comparación de distribuciones',30,160,1220,300);r.tablevisual('DriftCategorico',list(r.tables['DriftCategorico']),'Prueba y p-valor',30,490,1220,340)
 r.page('galeria','04 · Galería y comparaciones',[('Distribuciones','Variable'),('Distribuciones','Dataset')],note='Selecciona una variable. Intervalos comunes entre referencia y actual; proporciones evitan sesgo por tamaños 80/20.')
 r.chart('Distribuciones','Intervalo','KPI_Proporcion','Distribución relativa · referencia vs actual',30,160,1220,400,kind='line',legend='Dataset');r.tablevisual('Distribuciones',list(r.tables['Distribuciones']),'Frecuencias de cada intervalo',30,590,1220,240)
 r.page('correlaciones','05 · Correlaciones',[('Correlaciones','Dataset'),('Correlaciones','Variable2')],note='Selecciona Variable2 para explorar correlaciones con el target u otra característica. Correlación no implica causalidad.')
 r.chart('Correlaciones','Variable','KPI_Correlacion','Correlación Pearson · variable seleccionada',30,160,1220,330);r.tablevisual('Correlaciones',list(r.tables['Correlaciones']),'Matriz en formato largo',30,520,1220,310)
 return r.finish('| Streamlit | Power BI |\n|---|---|\n| Salud / target drift | KPIs y target por partición |\n| Drift numérico | KS, PSI y p-valores |\n| Drift categórico | Chi-cuadrado |\n| Galería / comparaciones | Distribuciones normalizadas en intervalos comunes |\n| Correlaciones | Ranking y matriz tabular filtrable |\n\nSplit estratificado idéntico al original, semilla 42. Las estadísticas se calculan en la exportación sobre el split completo. No se etiquetan como monitoreo de producción.')
if __name__=='__main__':
    print(m5())
