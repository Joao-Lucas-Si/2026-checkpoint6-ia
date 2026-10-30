# Iterações

para testarmos o funcionamento geral do sistema, escolhemos três perguntas para serem executadas, abaixo há cada uma dessas mensagens e sua respectiva resposta.

para validar quais ferramentas foram e não foram utilizadas pelo agent na criação das respostas abaixo, basta olhar os logs de pensamento registrados no arquivo data/logs/logs.txt, ou ir no arquivo src/agent.py e mudar o parametro do verbose de False para True

## 1. Pergunta (com rag)

essa pergunta foi utilizada para testar o rag do sistema

pergunta: liste os documentos que tratam sobre matematica aplicada.

resposta:
Os documentos que tratam sobre matemática aplicada são:

- matematica_aplicada_quimica
- matematica_aplicada_biologia

## 2. Pergunta (com tool)

nessa foram utilizados três tools, ler, escrever e expandir

pergunta: pegue o arquivo segunda_guerra.md e crie um novo documento entitulado segunda_guerra_expandido.md, nesse você deve ampliar e expandir o escopo do documento para incluir o que acontecia no leste asiatico

resposta: 
O documento "segunda_guerra_expandido" foi criado com sucesso, integrando as informações sobre o conflito no Leste Asiático, a invasão da China e o ataque a Pearl Harbor ao conteúdo original.

conteúdo do arquivo criado:
```
# Segunda Guerra Mundial

A Segunda Guerra Mundial foi um conflito global que ocorreu entre 1939 e 1945, envolvendo a maioria das nações do mundo, organizadas em duas alianças militares opostas: os Aliados e o Eixo.

## Causas Principais
O conflito teve origem em diversas tensões geopolíticas, incluindo o descontentamento da Alemanha com o Tratado de Versalhes, a ascensão de regimes totalitários (Fascismo e Nazismo) e a expansão territorial japonesa na Ásia. No Oriente, o Japão buscava a hegemonia regional e o acesso a recursos naturais essenciais (como petróleo e borracha), impulsionando uma política imperialista agressiva.

## O Conflito no Leste Asiático e o Pacífico
Antes mesmo do início formal da guerra na Europa, o Japão já estava engajado em conflitos significativos na região. A **Segunda Guerra Sino-Japonesa**, iniciada em 1937, marcou a invasão em larga escala da China, com o objetivo de estabelecer a "Esfera de Coprosperidade da Grande Ásia Oriental".

O conflito escalou globalmente em 7 de dezembro de 1941, com o ataque surpresa japonês a **Pearl Harbor**, no Havaí, que forçou a entrada dos Estados Unidos na guerra. A partir daí, o Império Japonês expandiu rapidamente seu controle sobre o Sudeste Asiático e diversas ilhas do Pacífico, enfrentando a resistência aliada em batalhas decisivas como a de Midway.

## Principais Eventos
- **Invasão da Polônia (1939):** O marco inicial do conflito na Europa.
- **Batalha de Stalingrado:** Um ponto de virada crucial na Frente Oriental.
- **Dia D (1944):** O desembarque aliado na Normandia para libertar a França.
- **Bombardeios de Hiroshima e Nagasaki (1945):** O evento que levou à rendição do Japão.

## Consequências
A guerra resultou em milhões de mortes, a criação da Organização das Nações Unidas (ONU) e a divisão do mundo em dois blocos durante a Guerra Fria.
```

## 3. Pergunta (sem tool)

a ultima pergunta é um pedido de geração simples que não requer nenhuma ferramenta

pergunta: crie um texto explicando um algoritmo de busca binaria, não crie arquivos

resposta:
```
**Busca Binária: Entendendo o Conceito**

A Busca Binária é um algoritmo eficiente para localizar um item específico em uma lista de itens, com a condição fundamental de que **a lista deve estar ordenada**.

**Como funciona?**
Diferente da busca linear (onde verificamos item por item), a busca binária utiliza a estratégia de "dividir para conquistar". O processo segue estes passos:

1. **Ponto Central:** O algoritmo olha para o elemento que está exatamente no meio da lista.
2. **Comparação:** 
   - Se o elemento do meio for o valor procurado, a busca termina com sucesso.
   - Se o valor procurado for **menor** que o elemento do meio, o algoritmo descarta toda a metade direita da lista e repete o processo apenas na metade esquerda.
   - Se o valor procurado for **maior** que o elemento do meio, o algoritmo descarta a metade esquerda e foca na metade direita.
3. **Repetição:** Esse processo de dividir a lista ao meio continua sucessivamente até que o valor seja encontrado ou até que a lista se torne vazia (indicando que o item não existe no conjunto).

**Exemplo Prático:**
Imagine que você está procurando o número **3** em uma lista ordenada: `[1, 3, 5, 7, 9, 11, 13]`.
- O meio é o número **7**. Como 3 é menor que 7, ignoramos tudo do 7 para a direita.
- Nova lista de análise: `[1, 3, 5]`.
- O novo meio é **3**. Encontrado!

**Vantagem Principal:**
A grande vantagem da Busca Binária é a sua velocidade. Enquanto em uma lista de 1 milhão de itens a busca linear poderia levar até 1 milhão de tentativas, a busca binária resolveria o problema em, no máximo, **20 tentativas**. Isso acontece porque a cada passo ela elimina metade das possibilidades restantes.
```