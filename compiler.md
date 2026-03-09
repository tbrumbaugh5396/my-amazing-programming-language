```mermaid

graph TD
    %% --- SOURCE AND FRONT-END ---
    A[Source Code] --> B[Tokenizer / Lexer]
    B --> C[Tokens]
    C --> D[Parser]
    D --> E[Expanded Abstract Syntax Tree - Expanded AST]
    E --> F[Macro Expander]
    F --> E

    %% --- GRAMMAR GUIDANCE ---
    G[EBNF / BNF Grammar Defintion] --> | Defines| A
    G --> | Guides | B
    G --> | Guides | D

    subgraph NAMESPACE_GRAPH["Graph-Native Namespaces"]
        N1[Namespace A]
        N2[Namespace B]
        N3[Namespace C]
        N1 --- N2
        N2 --- N3
        N1 --- N3
    end

    %% Context morphisms
    N1 --> |Morphisms| N2
    N2 --> |Morphisms| N3
    N3 --> |Morphisms| N1
    NAMESPACE_GRAPH --> |Resolves identifiers / types| H
    
    %% --- CONTEXT & NAMESPACES ---
    subgraph CONTEXT
        H[Context]
        H --> |Types / Contracts / Dependent Types| K
        H --> |HoTT Proofs / Equivalences| K
        H --> |Authority / Capabilities| K
    end
    
    H --> | Used for type checking and proofs | E
    F --> EE[Elaboration] --> J[High-Level / Semantic Intermediate Representation (Rich IR)]

    %% AST --> Elaboration --> RichIR[High-Level / Semantic IR (Rich IR)]
    %%RichIR --> E-Graph / Optimizer --> Optimized RichIR
    %%Optimized RichIR --> Lowering / Erasing --> CoreIR[Core IR / Low-Level IR]
    %%CoreIR 

    
    %% J --> K[Semantic Intermediate Representation - Semantic IR]
    H --> | Used for optimization and verification | K
    
    %% --- SEMANTIC OPTIMIZER / E-GRAPH ---
    H --> J[E-Graph / Equivalence Graph]
    J --> K[Cost Model & Extractor]
    K --> L[Optimized Rich IR]

    %% --- LOWERING / ERASING TO CORE IR ---
    L --> M[Lowering / Erasing]
    M --> N[Core IR / Low-Level IR]
    

    %% --- BACKEND / MACH LEVEL ---
    subgraph BACKEND
        O[Low-Level IR / Mach-Level IR]
        P[Instruction Selection]
        Q[Register Allocation]
        R[Pipeline Scheduling / Optimization]
        S[Target Assembly / Machine Code]
    end

    N --> O
    O --> P --> Q --> R --> S
    S --> T[Executable / Target Runtime]
    


```
