---
marp        : true

title       : Removendo Tendências e Isolando Ciclos
author      : Gabriel Cintra
description : This is a presentation for research group of Applied Macroeconomics - UData UDESC.
keywords    : macroeconomia aplicada, grupo de pesquisa, udata.
paginate    : true
admonition  : true
theme       : godel
---
<style>

   .cite-author {     
      text-align        : right; 
   }
   .cite-author:after {
      color             : white;
      font-size         : 125%;
      font-style        : italic;
      font-weight       : bold;
      font-family       : Cambria, Cochin, Georgia, Times, 'Times New Roman', serif; 
      padding-right     : 130px;
   }
   .cite-author[data-text]:after {
      content           : " - "attr(data-text) " - ";      
   }

   .cite-author p {
      padding-bottom : 40px
   }

  .two-column {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .left-column {
    flex: 1;
    padding-right: 20px;
  }
  .right-column {
    flex: 1;
    text-align: center;
  }
  img {
    width: 100%;
    max-width: 600px;
  }
</style>

<!-- _class: titlepage -->

![bg left:33% grayscale:0 brightness:1.1](./static/cover.webp)

<div class="title"         > Ciclos Econômicos </div>
<div class="subtitle"      > Removendo tendências e isolando ciclos               </div>
<div class="author"        > Gabriel Cintra                 </div>
<div class="date"          > Florianópolis, Outubro 2023               </div>
<div class="organization"  > UDESC - ESAG.     </div>

---

# Agenda

<div class="columns">
<div>
      
<!-- _class: cool-list -->

1. _Caracterização de Sistemas_
2. _Dados Empíricos_
3. _Removendo Tendências - Parte 1_
4. _Removendo Tendências - Parte 2_

</div>  
<div>    
        
 

</div> 
</div>           
            
---                   
<!-- _class: transition -->  

Removendo Tendências - Parte 2

---

# Removendo tendências: Detrending

Detrending linear. Assumimos: $y_t = y_0 (1 + g_y)^t e^{u_t}$

<div class="two-column">
  <div class="left-column">

Tendência:
- $\hat{\log y}_t = \hat{\alpha}_0 + \hat{\alpha}_1 t$
- $\hat{\alpha}_0= 4.566464273572031$
- $\hat{\alpha}_1= 0.004211711391038625$

Série sem tendência:
- $\tilde{y}_t = \hat{u}_t = \log y_t - \hat{\log y}_t$

  </div>
  <div class="right-column">
    <img src="./static/apresentacao2/0-plot_5_years_log_tendencia_exp.png"/>
  </div>
</div>

---

# Removendo tendências: Detrending

Série log linearizada sem tendência: $\tilde{y}_t = \hat{u}_t = \log y_t - \hat{\log y}_t$

<div class="two-column">
  <div class="left-column">

A série resultante claramente não é  **CSSP**.

O problema está na:
- *Baixa frequência amostral?*
- *Período amostral insuficiente?*
- *Método utilizado?*

  </div>
  <div class="right-column">
    <img src="./static/apresentacao2/0-plot_5_years_log_tendencia_rem.png"/>
  </div>
</div>

---

# Removendo tendências: Detrending

Série log linearizada sem tendência: $\tilde{y}_t = \hat{u}_t = \log y_t - \hat{\log y}_t$

<div class="two-column">
  <div class="left-column">

Detrending amostragem 5 anos:
- $\alpha_0 = 96.2$
- $\alpha_1 = 42.1 \cdot 10^{-4}$

Detrending amostragem anual:
- $\alpha_0 = 98.9$
- $\alpha_1 = 43.0 \cdot 10^{-4}$

  </div>
  <div class="right-column">
    <img src="./static/apresentacao3/0-plot_2.png"/>
  </div>
</div>

---

# Removendo tendências: Detrending

Série log linearizada sem tendência: $\tilde{y}_t = \hat{u}_t = \log y_t - \hat{\log y}_t$

<div class="two-column">
  <div class="left-column">

Detrending amostragem 5 anos:
- $\alpha_0 = 96.2$
- $\alpha_1 = 42.1 \cdot 10^{-4}$

Detrending amostragem anual:
- $\alpha_0 = 98.9$
- $\alpha_1 = 43.0 \cdot 10^{-4}$

  </div>
  <div class="right-column">
    <img src="./static/apresentacao3/0-plot_3.png"/>
  </div>
</div>

---
# Removendo tendências: Detrending

Série log linearizada sem tendência: $\tilde{y}_t = \hat{u}_t = \log y_t - \hat{\log y}_t$

<div class="two-column">
  <div class="left-column">

Detrending amostragem 5 anos:
- $\alpha_0 = 96.2$
- $\alpha_1 = 42.1 \cdot 10^{-4}$
Detrending amostragem anual:
- $\alpha_0 = 98.9$
- $\alpha_1 = 43.0 \cdot 10^{-4}$
Detrending amostragem trimestral:
- $\alpha_0 = 98.1$
- $\alpha_1 = 46.8 \cdot 10^{-4}$

  </div>
  <div class="right-column">
    <img src="./static/apresentacao3/0-plot_4.png"/>
  </div>
</div>

---

# Removendo tendências: Detrending

<div class="two-column">
  <div class="left-column">
<img src="./static/apresentacao3/4-plot_all_components1.png"/>
  </div>
  <div class="right-column">
    <img src="./static/apresentacao3/5-plot_all_components2.png"/>
  </div>
</div>

---

# Removendo tendências: Diferenciação


---
<!-- _class: transition3 -->  

 Obrigado!
    
![bg left:50% grayscale:0](./static/cover1.webp)