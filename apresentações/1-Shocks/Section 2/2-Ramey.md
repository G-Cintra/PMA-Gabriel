---
marp        : true

title       : Macroeconomic Shocks and Their Propagation
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
</style>

<!-- _class: titlepage -->

![bg left:33% grayscale:0 brightness:1.1](./static/cover.webp)

<div class="title"         > Macroeconomic Shocks and Their Propagation - V.A. Ramey </div>
<div class="subtitle"      > 2. METHODS FOR IDENTIFYING SHOCKS AND ESTIMATING IMPULSE
RESPONSES</div>
<div class="author"        > Gabriel Cintra                 </div>
<div class="date"          > Florianópolis, Novembro 2024             </div>
<div class="organization"  > UDESC - ESAG.     </div>

---

# Agenda

     
<!-- _class: cool-list -->

1. _O que é um Choque_
2. _Identificação de choques com o método de decomposição de Cholesky_

  
---
# O que é um choque?

Um **choque** deve ser uma força primitiva exógena, **representativa economicamente**, e que:

1. **Seja exógeno** em relação às variáveis endógenas do modelo (atuais e defasadas);
2. **Não seja correlacionado** com outros choques exógenos;
3. **Represente movimentos inesperados** em variáveis exógenas.

Essas características são essenciais para identificar efeitos causais únicos.

---
# Choques primitivos vs. respostas endógenas

- Choques primitivos podem afetar diretamente várias equações do sistema.
- Exemplo: Um evento geopolítico (choque primitivo) pode levar a:
  - Guerra (impacto econômico direto);
  - Respostas endógenas de políticas fiscal e monetária.

⚠️ Choques correlacionados, como políticas fiscal e monetária reagindo ao mesmo evento, **não são choques primitivos**, mas respostas endógenas ao choque.

---
# Modelo Estrutural Simples

O modelo estrutural descreve as relações econômicas fundamentais entre três variáveis:

- $\tau_t$: Impostos.
- $g_t$: Gastos do governo.
- $y_t$: PIB.

As relações estruturais são descritas por:

$$
\tau_t = b_{\tau g} g_t + b_{\tau y} y_t + \varepsilon_{\tau t},
$$

$$
g_t = b_{g \tau} \tau_t + b_{g y} y_t + \varepsilon_{g t},
$$

$$
y_t = b_{y \tau} \tau_t + b_{y g} g_t + \varepsilon_{y t}.
$$

---
# Choques Estruturais

- Os coeficientes $b_{ij}$ representam como uma variável afeta outra.

- Os choques estruturais são:
  - $\varepsilon_{\tau t}$: Choque em impostos.
  - $\varepsilon_{g t}$: Choque em gastos.
  - $\varepsilon_{y t}$: Choque no PIB.

Esses choques têm as seguintes características:
1. **Exógenos**: Não são influenciados pelas variáveis endógenas do sistema.
2. **Não correlacionados**: São estatisticamente independentes entre si.

---
# Problema de Identificação

Os coeficientes $b_{ij}$ e os choques estruturais $\varepsilon_t$ **não podem ser identificados diretamente** porque:

1. As variáveis endógenas ($\tau_t$, $g_t$, $y_t$) **interagem simultaneamente**.
2. O impacto contemporâneo de cada variável sobre as outras é confuso devido à **correlação mútua**.

### Exemplo:
- Se o PIB ($y_t$) aumenta, os impostos ($\tau_t$) e os gastos ($g_t$) podem mudar simultaneamente.
- É difícil determinar:
  - Se essas mudanças são causadas por **choques exógenos** ($\varepsilon_{\tau t}$, $\varepsilon_{g t}$).
  - Ou se são resultado de **interações endógenas** entre as variáveis.

---
# Modelo Dinâmico com Defasagens

Para resolver o problema de identificação, o modelo é ampliado para incluir uma **dinâmica temporal**: As variáveis de hoje dependem das variáveis passadas e dos choques exógenos.

As variáveis econômicas frequentemente não respondem **imediatamente** a choques exógenos. Exemplos:

- Um aumento na **taxa de juros** hoje pode levar meses para afetar o **PIB** e a **inflação**.
- Uma mudança no **gasto público** pode demorar vários trimestres para impactar a **produção**.

O **modelo dinâmico com defasagens** reflete essa realidade, permitindo que os efeitos dos choques sejam distribuídos ao longo do tempo.

---
# Modelo Estrutural dinâmico

O modelo estrutural dinâmico pode ser representado na forma:

$$
Y_t = B(L) Y_t + \Omega \varepsilon_t,
$$

onde:
- $Y_t$: **Vetor das variáveis** endógenas. Ex: $[\tau_t, g_t, y_t]'$:  (impostos, gastos e PIB).
- $B(L)$: **Polinômio de defasagens** que descreve as interações passadas: $B_0,B_1,...,B_p$
- $\Omega$: **Matriz de impacto contemporâneo** dos choques estruturais $\varepsilon_t$, define quais variáveis cada choque irá influenciar.
---
# Modelo Estrutural dinâmico

Dado:

$$
Y_t = B(L) Y_t + \Omega \varepsilon_t,
$$

Para um modelo de primeira ordem:

$$B(L) = B_0 + B_1L$$

Substituindo explicitamente as defasagens no modelo, temos:

$$Y_t = B_0Y_t + B_1Y_{t-1} + \Omega \varepsilon_t$$

---
# Reorganizando o Modelo

Reorganizando para evidenciar $Y_t$:
$$
Y_t = B_0Y_t + B_1Y_{t-1} + \Omega \varepsilon_t
$$
$$
(I - B_0)Y_t = B_1Y_{t-1} + \Omega \varepsilon_t
$$

Finalmente, resolvendo para $Y_t$:

$$
Y_t = B_1(I - B_0)^{-1}Y_{t-1} + \Omega(I - B_0)^{-1}\varepsilon_t
$$

---
# Modelo na forma reduzida

$$
Y_t = B_1(I - B_0)^{-1}Y_{t-1} + \Omega(I - B_0)^{-1}\varepsilon_t
$$

Forma reduzida:

$$
Y_t = A_1Y_{t-1} + H\varepsilon_t
$$

- $A_1 = B_1(I - B_0)^{-1}$: Coeficientes reduzidos associados às variáveis defasadas.
- $H = \Omega(I - B_0)^{-1}$: Matriz de impacto dos choques estruturais.

Este modelo fornece uma base para estimar os efeitos das defasagens e identificar os choques estruturais ($\varepsilon_t$).

---
# Proposta de Valores para $B_0$, $B_1$ e $\Omega$

Para o exemplo econômico com PIB ($Y_{1t}$) e Taxa de Juros ($Y_{2t}$), definimos o vetor de variáveis endógenas como:

$$
Y_t = \begin{bmatrix} Y_{1t} \\ Y_{2t} \end{bmatrix}.
$$

Proposta de valores:

$$
B_0 = \begin{bmatrix}
0 & -0.2 \\
0.1 & 0
\end{bmatrix}, \quad
B_1 = \begin{bmatrix}
0.4 & 0 \\
0 & 0.3
\end{bmatrix}, \quad
\Omega = \begin{bmatrix}
1 & 0 \\
0.2 & 1
\end{bmatrix}.
$$

---
# Interpretação dos Valores

Proposta de valores:

$$
B_0 = \begin{bmatrix}
0 & -0.2 \\
0.1 & 0
\end{bmatrix}, \quad
B_1 = \begin{bmatrix}
0.4 & 0 \\
0 & 0.3
\end{bmatrix}, \quad
\Omega = \begin{bmatrix}
1 & 0 \\
0.2 & 1
\end{bmatrix}.
$$

- **$B_0$: Interações contemporâneas**:
  - $b_{12} = -0.2$: Um aumento na Taxa de Juros ($Y_{2t}$) reduz o PIB ($Y_{1t}$) contemporaneamente.
  - $b_{21} = 0.1$: O PIB ($Y_{1t}$) influencia positivamente a Taxa de Juros ($Y_{2t}$) contemporaneamente.
  - $b_{11} = b_{22} = 0$: Nenhuma variável influencia a si mesma contemporaneamente.

---
# Interpretação dos Valores

Proposta de valores:

$$
B_0 = \begin{bmatrix}
0 & -0.2 \\
0.1 & 0
\end{bmatrix}, \quad
B_1 = \begin{bmatrix}
0.4 & 0 \\
0 & 0.3
\end{bmatrix}, \quad
\Omega = \begin{bmatrix}
1 & 0 \\
0.2 & 1
\end{bmatrix}.
$$

- **$B_1$: Efeitos defasados**:
  - $b_{11} = 0.4$: O PIB no período anterior ($Y_{1,t-1}$) contribui significativamente para o PIB atual ($Y_{1t}$).
  - $b_{22} = 0.3$: A Taxa de Juros defasada ($Y_{2,t-1}$) afeta moderadamente a própria taxa no período atual ($Y_{2t}$).
  - $b_{12} = b_{21} = 0$: Não há efeitos defasados cruzados entre PIB e Taxa de Juros.

---
# Interpretação dos Valores

Proposta de valores:

$$
B_0 = \begin{bmatrix}
0 & -0.2 \\
0.1 & 0
\end{bmatrix}, \quad
B_1 = \begin{bmatrix}
0.4 & 0 \\
0 & 0.3
\end{bmatrix}, \quad
\Omega = \begin{bmatrix}
1 & 0 \\
0.2 & 1
\end{bmatrix}.
$$

- **$\Omega$: Impacto dos choques estruturais ($\varepsilon_t$)**:
  - $\omega_{11} = 1$: Choques no PIB têm impacto direto no PIB.
  - $\omega_{22} = 1$: Choques na Taxa de Juros têm impacto direto na própria taxa.
  - $\omega_{21} = 0.2$: Choques na Taxa de Juros afetam moderadamente o PIB.
  - $\omega_{12} = 0.2$: Choques no PIB não afetam a taxa de juros.
---
# Cálculo de $A_1$ e $H$

A forma reduzida do modelo é:

$$
Y_t = A_1Y_{t-1} + H\varepsilon_t,
$$

Coeficientes reduzidos $A_1$:
$$
A_1 = B_1(I - B_0)^{-1} = \begin{bmatrix}
0.3922 & -0.0784 \\
0.0294 & 0.2941
\end{bmatrix}.
$$

Matriz de impacto $H$:
$$
H = \Omega(I - B_0)^{-1} = \begin{bmatrix}
0.9804 & -0.1961 \\
0.2941 & 0.9412
\end{bmatrix}.
$$

---
# Valores Propostos para 5 Períodos

Propomos os seguintes valores empíricos para as variáveis endógenas:

| Período | PIB ($Y_{1t}$) | Taxa de Juros ($Y_{2t}$) |
|---------|----------------|--------------------------|
| 1       | 100            | 5.0                      |
| 2       | 102            | 4.8                      |
| 3       | 101            | 4.9                      |
| 4       | 103            | 5.1                      |
| 5       | 104            | 5.2                      |

---

# Cálculo dos Choques Estruturais

A forma reduzida do modelo é:

$$
Y_t = A_1Y_{t-1} + H\varepsilon_t.
$$

Rearranjando para encontrar os choques estruturais:

$$
\varepsilon_t = H^{-1}(Y_t - A_1Y_{t-1}).
$$

---
# Resultados:

$$
\varepsilon_2 = \begin{bmatrix} 60.73 \\ -18.56 \end{bmatrix}.
$$
$$
\varepsilon_3 = \begin{bmatrix} 59.02 \\ -17.92 \end{bmatrix}.
$$
$$
\varepsilon_4 = \begin{bmatrix} 61.36 \\ -18.44 \end{bmatrix}.
$$
$$
\varepsilon_5 = \begin{bmatrix} 61.58 \\ -18.53 \end{bmatrix}.
$$