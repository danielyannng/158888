# Geo-located NLP Feedback System for Public Transport: A Shanghai Case Study

**Course:** 158.888 Information Technology Research Project  
**Group:** G8  
**System name:** Shanghai Transit Intelligence  
**Case study:** Shanghai metro and bus services  
**Main technologies:** Natural Language Processing, Geographic Information Systems, FastAPI, Streamlit, SQLite, Folium, QGIS, DBSCAN, Moran's I  

---

## 1 Introduction

### 1.1 Background

Public transport plays a fundamental role in supporting urban development and sustainable mobility. Efficient transport systems help reduce traffic congestion, improve accessibility, and support economic and social activities within cities. In large metropolitan cities, public transport serves as an essential component of urban infrastructure by connecting residential areas, commercial districts, educational institutions, and transport hubs. As cities continue to expand and urban populations increase, maintaining the effectiveness and reliability of public transport systems has become an increasingly important challenge for governments, transport operators, and city planners (Eboli & Mazzulla, 2007). Shanghai is one of the world's major metropolitan cities and operates a highly developed public transport system consisting of metro and bus services. Over the past two decades, the city has continuously expanded its public transport infrastructure, resulting in the development of a large-scale metro system alongside an extensive bus network. Together, metro and bus services form the backbone of daily mobility within the city and support millions of passenger journeys each day. The integration of different transport modes has become essential for facilitating efficient travel and supporting sustainable urban mobility (Dou et al., 2024). At the same time, rapid advances in digital communication technologies have transformed the way passengers interact with transport services and express their travel experiences. Traditional methods of collecting passenger feedback, such as surveys and customer service channels, are increasingly complemented by online platforms where users voluntarily share opinions and experiences. Social media platforms, online review websites, discussion forums, and mobile applications have become important sources of user-generated content (Kaplan & Haenlein, 2010). Through these platforms, passengers frequently discuss issues such as delays, overcrowding, transfer convenience, accessibility, cleanliness, safety, ticketing systems, and service quality. The growing availability of online feedback has created new opportunities for transport research and service evaluation. Compared with traditional survey-based approaches, online user-generated content can provide a larger volume of feedback, reflect more diverse perspectives, and capture experiences closer to real travel situations. Recent research has demonstrated that online reviews can reveal meaningful insights into how passengers perceive public transport services and identify factors that influence overall service satisfaction (Dou et al., 2024). As a

result, user-generated content is increasingly recognised as a valuable data source for understanding passenger experiences and evaluating transport performance. However, the increasing volume of online feedback also introduces new challenges. Most transport-related comments are stored as unstructured textual data distributed across multiple online platforms. Unlike structured survey responses, these comments are often difficult to analyse systematically. The scale of available data makes manual review inefficient and impractical, particularly when thousands of comments are generated over relatively short periods of time. Consequently, there is a growing need for computational approaches capable of processing large volumes of textual information and transforming them into meaningful insights (Aggarwal & Zhai, 2012). Recent advances in data analytics, machine learning, and geospatial technologies provide promising opportunities to address these challenges. In particular, Natural Language Processing (NLP) enables the automatic analysis of textual data through techniques such as text classification, sentiment analysis, and keyword extraction (Jurafsky & Martin, 2024). At the same time, Geographic Information Systems (GIS) allow information to be visualised spatially and support the identification of geographic patterns and spatial relationships. Previous research has highlighted that urban mobility visualisation systems can support the interpretation of complex transport datasets through interactive and spatial approaches (Sobral et al., 2019). Therefore, the integration of NLP and GIS provides an opportunity to transform large collections of transport-related comments into interpretable spatial information that can support urban mobility research. Furthermore, the integration of digital technologies into urban management has become a central objective of smart-city initiatives. Smart cities seek to leverage data, digital infrastructure, and advanced analytics to improve public services and enhance the quality of urban life (Batty et al., 2012). Public transport systems represent a critical component of smart-city development because they directly influence mobility, accessibility, and sustainability. Within this context, analysing transport-related user feedback through integrated NLP and GIS approaches has the potential to provide valuable insights into service performance and passenger needs while supporting more evidence-based decision-making processes.

### 1.2 Problem Statement

Although large amounts of transport-related feedback are publicly available, significant challenges remain in effectively extracting and utilising information from these data sources. Traditional approaches to transport service evaluation have relied heavily on passenger

satisfaction surveys, official complaint systems, customer service records, and periodic performance assessments. While these methods continue to provide valuable information, they often require substantial time, financial resources, and organisational effort to implement. In addition, survey-based approaches may suffer from limited sample sizes, response bias, and relatively low participation rates, potentially restricting their ability to capture the full diversity of passenger experiences (Eboli & Mazzulla, 2007). In contrast, online platforms generate large volumes of unsolicited user feedback on a daily basis. Passengers can share opinions immediately after travel experiences, providing a rich source of real-world information regarding transport services. Previous research has shown that online reviews and digital feedback can provide valuable insights into customer perceptions and service experiences (Cheung & Thadani, 2012). However, the sheer volume of available comments presents a new analytical challenge. Thousands of comments may be distributed across multiple platforms, making manual review and interpretation impractical. Furthermore, online comments often contain informal language, abbreviations, spelling variations, emojis, slang expressions, and mixed sentiments, increasing the complexity of analysis. Another challenge arises from the unstructured nature of textual feedback. Although user comments contain valuable information about service quality and passenger concerns, these insights are often hidden within large collections of text. Without automated analytical methods, identifying recurring themes, common complaints, or overall sentiment patterns becomes extremely difficult. As a result, much potentially useful information remains underutilised despite its relevance to transport planning and service improvement. Text mining approaches have therefore become increasingly important for extracting useful information from large-scale unstructured textual datasets (Aggarwal & Zhai, 2012). At the same time, existing transport network datasets are primarily designed to describe physical infrastructure. These datasets commonly contain information relating to routes, stations, stops, administrative boundaries, and network connectivity. While such datasets provide essential geographic information, they generally do not capture passenger perceptions, experiences, or opinions. Consequently, transport operators and researchers often possess detailed information about the structure of transport networks but have limited understanding of how users experience those networks in practice. This situation creates a disconnect between transport feedback analysis and spatial transport analysis. Textual feedback may reveal what passengers are concerned about, while transport datasets reveal where infrastructure is located. However, without establishing a connection between these two forms of information, it is difficult to determine where specific issues occur and how concerns vary across different parts of the transport network. For example, passengers may frequently complain about overcrowding, delays, or transfer difficulties, but the geographic distribution of these concerns may remain unclear if comments are not linked to specific locations.

In addition, many existing studies focus primarily on either textual analysis or spatial analysis rather than integrating both approaches within a single analytical framework. Research involving online transport reviews often emphasises sentiment analysis and opinion mining, whereas GIS-based studies typically focus on transport infrastructure and spatial patterns. Interactive spatial visualisation approaches have demonstrated potential for improving the interpretation of complex urban mobility data, but integration between textual feedback analysis and geographic visualisation remains an ongoing research challenge (Sobral et al., 2019). Therefore, there is a need for an integrated approach capable of combining transport-related textual feedback with geographic transport data. Such an approach should enable the automatic identification of passenger concerns, connect these concerns to specific locations within the transport network, and provide intuitive visualisation tools that support interpretation and exploration. Addressing this gap forms the central motivation of the present project and provides the foundation for developing a Geo-located NLP Feedback System for Public Transport.

### 1.3 Research Motivation

The rapid development of machine learning, data analytics, and geospatial technologies has significantly improved the ability to process large-scale textual and spatial datasets. In recent years, Natural Language Processing (NLP) has become one of the most widely adopted approaches for analysing user-generated content and extracting meaningful information from large collections of text. NLP provides computational methods that enable machines to process, analyse, and extract information from human language data (Jurafsky & Martin, 2024). Techniques such as text classification, sentiment analysis, keyword extraction, and opinion mining have been successfully applied in domains including customer satisfaction analysis, social media monitoring, public opinion evaluation, and service quality assessment. These methods enable researchers to identify recurring themes, detect sentiment patterns, and understand user concerns without relying on time-consuming manual review processes (Aggarwal & Zhai, 2012). Within the context of transport research, NLP techniques have increasingly been used to analyse passenger feedback and evaluate public transport services. Recent studies have demonstrated that online reviews can provide valuable insights into passenger perceptions of transport quality and reveal factors influencing service satisfaction (Dou et al., 2024). By analysing transport-related comments, researchers can identify commonly discussed issues such as delays, overcrowding, transfer convenience, accessibility, and service reliability. However, while NLP can effectively identify what passengers are discussing, it provides limited information regarding where these issues occur within the transport network. At the same time, Geographic Information Systems (GIS) have become essential tools for managing, analysing, and visualising spatial information. GIS technologies enable researchers to

integrate different datasets, analyse geographic relationships, and identify spatial patterns through interactive maps and visualisation techniques. In the field of transport planning, GIS has been widely applied to route analysis, accessibility assessment, traffic management, and mobility visualisation. Recent developments in web-based GIS technologies have further improved the accessibility of spatial information by enabling users to interact with geographic data through online dashboards and web mapping applications (Sobral et al., 2019). Although NLP and GIS have both demonstrated significant value independently, integrating these technologies offers opportunities to generate deeper insights into public transport systems. NLP can identify the content and sentiment of passenger feedback, while GIS can reveal the spatial distribution of those concerns. Combining these approaches enables researchers to answer not only what problems passengers experience but also where those problems are concentrated. Such integration supports a more comprehensive understanding of transport service performance and can provide decision-makers with more actionable information. The motivation for this project also stems from the growing emphasis on smart-city development and data-driven urban governance. Smart-city initiatives seek to utilise advanced technologies and urban data to improve public services, increase operational efficiency, and enhance citizen engagement. Data-driven approaches have become an important foundation for future smart cities because they allow urban systems to collect, integrate, and analyse information from multiple sources (Batty et al., 2012; Zheng et al., 2014). Public transport systems are central to these objectives because they directly affect mobility, accessibility, sustainability, and quality of life. As cities continue to generate increasing volumes of digital data, there is a growing need for analytical tools capable of transforming raw information into meaningful knowledge that can support urban decision-making. Existing research has often focused on either textual analysis or spatial analysis in isolation. Studies involving online transport reviews commonly emphasise sentiment analysis and opinion extraction, while GIS-based research generally focuses on spatial patterns and infrastructure analysis. Relatively fewer studies have developed practical systems that combine online passenger feedback, transport network data, NLP analysis, GIS visualisation, and interactive web technologies within a single platform. This research gap provides an opportunity to explore how integrated analytical approaches can enhance the interpretation and communication of transport-related information. Motivated by these challenges and opportunities, this project proposes the development of a Geo-located NLP Feedback System for Public Transport using Shanghai as a case-study city. By combining publicly available user comments, transport network datasets, NLP analysis techniques, GIS-based spatial processing, and interactive web visualisation, the project seeks to create a practical prototype capable of transforming unstructured transport feedback into meaningful geographic insights.

### 1.4 Project Aim and Objectives

The aim of this project is to develop a web-based Geo-located NLP Feedback System for Public Transport using Shanghai as the case-study city. The project focuses on two major public transport modes, namely metro and bus services, and seeks to integrate publicly available user feedback with real transport network data. Through the combination of Natural Language Processing (NLP), Geographic Information Systems (GIS), and interactive web technologies, the proposed system aims to transform unstructured transport-related comments into meaningful spatial insights that can support transport analysis and urban mobility research. To achieve this aim, the project pursues the following objectives:

1. To collect and organise publicly available user-generated comments relating to Shanghai

metro and bus services.

2. To collect, prepare, and standardise transport network datasets, including metro lines,

metro stations, bus routes, bus stops, and district boundaries.

3. To apply NLP techniques such as text classification, sentiment analysis, and keyword

extraction to identify major passenger concerns and transport-related issues.

4. To establish connections between textual feedback and geographic transport objects

through route names, station names, stop names, and district references.

5. To conduct spatial analyses, including clustering and spatial pattern identification, to

investigate the geographic distribution of transport-related concerns.

6. To develop an interactive web-based dashboard that allows users to explore transport

feedback through maps, filters, and visual analytics.

7. To evaluate the effectiveness of integrating NLP and GIS for supporting public transport

service analysis and smart-city applications. Based on these objectives, the project addresses the following research questions:

RQ1: What transport-related issues are most frequently discussed by metro and bus users in

Shanghai?

RQ2: Where are these issues geographically concentrated across the public transport network?

RQ3: How can NLP and GIS technologies be integrated to improve the interpretation and

visualisation of transport-related user feedback?

RQ4: To what extent can an interactive web-based system support the exploration and

understanding of public transport issues? The answers to these research questions will contribute to the development of a practical framework for integrating textual feedback analysis and spatial transport analysis. The resulting

system is expected to demonstrate how user-generated content can be transformed into actionable spatial information that supports transport planning, service evaluation, and smart-city decision-making.

### 1.5 Project Scope

This project focuses on Shanghai, China, as the selected case-study city and investigates two major public transport modes: metro and bus services. Shanghai was selected because it possesses one of the largest and most complex public transport networks in the world, providing a suitable environment for exploring the integration of transport-related user feedback and geospatial analysis. The city's extensive transport infrastructure and large passenger population generate substantial amounts of publicly available transport-related information, making it an appropriate case for the development and evaluation of a geo-located feedback system. The project primarily relies on publicly available user-generated content and open transport network datasets. User-generated content may include online reviews, comments, suggestions, and complaints relating to passenger experiences within metro and bus services. These textual data serve as the primary source for Natural Language Processing (NLP) analysis. Transport network datasets include metro lines, metro stations, bus routes, bus stops, and district boundaries, which provide the spatial foundation for Geographic Information System (GIS) analysis and visualisation. The scope of the project is limited to secondary data analysis and does not involve direct interaction with human participants. No questionnaires, interviews, focus groups, or behavioural experiments are conducted during the study. Instead, the project focuses on analysing publicly accessible information that has already been generated by users through online platforms. To ensure ethical compliance, personally identifiable information is excluded from analysis, and the project emphasises aggregated insights rather than individual-level observations. From a technical perspective, the project aims to develop a demonstrable prototype rather than a fully operational commercial platform. The proposed system is designed to illustrate the integration of NLP, GIS, and web technologies within an academic project environment. While the system is capable of processing transport-related feedback and visualising analytical results, it is not intended to replace professional transport management systems or real-time operational platforms. Several limitations also define the scope of the project. First, the analysis focuses only on metro and bus services and does not include other transport modes such as taxis, ride-sharing services, bicycles, or ferries. Second, the project relies on publicly available user comments, meaning that findings may be influenced by the characteristics and biases of online users. Third, due to time and resource constraints, the project focuses on the development of a proof-of-concept prototype rather than a large-scale production-ready system. Despite these limitations, the project provides

a practical demonstration of how textual feedback and spatial information can be integrated within a smart-city context.

### 1.6 Project Contributions

This project contributes to the fields of transport informatics, urban analytics, spatial analysis, and smart-city applications through the development of an integrated Geo-located NLP Feedback System for Public Transport. The first contribution is the integration of Natural Language Processing and Geographic Information Systems within a unified analytical framework. Previous studies have often focused on either textual analysis or spatial analysis independently. In contrast, this project combines these approaches by linking user-generated transport feedback with geographic transport infrastructure. This integration enables both thematic and spatial interpretations of passenger concerns. The second contribution is the development of a practical methodology for transforming unstructured online feedback into structured analytical information. Through the application of text classification, sentiment analysis, and keyword extraction techniques, the system is able to identify major transport-related issues and organise large volumes of user-generated content into interpretable categories. This approach demonstrates how NLP can support the analysis of transport service quality using publicly available data sources. The third contribution lies in the incorporation of spatial analytical techniques to examine the geographic distribution of passenger concerns. The project applies clustering analysis and spatial pattern analysis to investigate how transport-related issues are distributed across different locations within the transport network. By identifying areas where particular concerns are concentrated, the project provides a spatial perspective that is often missing from conventional text-based analyses. The fourth contribution is the development of an interactive web-based dashboard that combines transport network data, textual insights, and spatial visualisation within a single user-centred platform. Through interactive maps, filtering functions, and visual analytics components, users can explore transport-related issues dynamically rather than relying solely on static reports. This contribution demonstrates the value of integrating analytical outputs into accessible visual interfaces. The fifth contribution is the provision of a practical case study based on Shanghai's metro and bus systems. While the proposed framework is developed using Shanghai as the case-study city, the overall methodology may also be adapted to other urban environments. As a result, the project contributes not only a functional prototype but also a transferable analytical framework that may support future smart-city and urban mobility applications.

Finally, the project contributes to the growing body of research exploring data-driven approaches to urban management. By demonstrating how publicly available user feedback can be transformed into meaningful spatial information, the project highlights the potential of integrating digital technologies and citizen-generated data to support evidence-based decision-making.

### 1.7 Report Structure

The remainder of this report is organised into eight chapters. Chapter 2 presents a comprehensive review of literature related to public transport service evaluation, user-generated content, Natural Language Processing, Geographic Information Systems, spatial analysis, and smart-city applications. The chapter identifies key theoretical foundations, methodological approaches, and research gaps relevant to the present study. Chapter 3 describes the overall research methodology adopted in the project. It outlines the research design, data collection procedures, data processing workflow, NLP techniques, GIS analytical methods, and system architecture used to develop the proposed framework. Chapter 4 focuses on data collection and preparation. The chapter introduces the datasets used in the project, explains the procedures for data cleaning and preprocessing, and describes how transport-related textual data are prepared for analysis and linked with spatial transport datasets. Chapter 5 presents the Natural Language Processing component of the project. The chapter describes the implementation of text classification, sentiment analysis, and keyword extraction techniques, followed by model evaluation and analysis of transport-related feedback. Chapter 6 discusses the spatial analysis component of the project. It presents the methods used to connect textual feedback with geographic locations and examines the spatial distribution of transport-related issues through clustering and spatial pattern analysis. Chapter 7 introduces the implementation of the web-based prototype system. The chapter explains the system architecture, backend and frontend components, dashboard design, user interaction workflow, and visualisation functionalities. Chapter 8 provides a discussion of the findings obtained from the project. It evaluates the strengths and limitations of the proposed approach, reflects on methodological challenges, and identifies opportunities for future improvements and extensions. Finally, Chapter 9 concludes the report by summarising the major findings, contributions, and implications of the study. The chapter also highlights how the proposed system contributes to transport analysis, urban mobility research, and smart-city development.

## 2 Literature Review

### 2.1 Public Transport Service Quality and Passenger Feedback

Public transport service quality has long been recognised as one of the most important factors influencing passenger satisfaction, travel behaviour, and the overall effectiveness of urban transport systems. As urban populations continue to grow and cities become increasingly dependent on public transport, understanding how passengers evaluate transport services has become an important research topic for transport operators, planners, and policymakers. Service quality not only affects passenger experiences but also influences public transport usage, mode choice, and long-term transport sustainability (Eboli & Mazzulla, 2007). Traditionally, public transport service quality has been evaluated using a combination of operational performance indicators and passenger satisfaction surveys. Operational indicators often include measures such as punctuality, reliability, travel time, service frequency, and vehicle occupancy. While these indicators provide valuable information about system performance, they do not necessarily reflect how passengers perceive transport services. Passenger satisfaction studies have therefore become an important method for understanding perceived service quality because operational indicators alone cannot fully explain user experiences (de Oña & de Oña, 2015). Eboli and Mazzulla (2007) identified several service quality attributes that significantly influence passenger satisfaction in bus transport systems, including reliability, comfort, cleanliness, security, and information availability. Their findings suggest that passengers evaluate transport services based on both functional performance and subjective travel experiences. Similar conclusions have been reported in subsequent studies, which highlight that perceived service quality often differs from objective operational performance measures (Nathanail, 2008). Among the various dimensions of transport service quality, reliability has consistently emerged as one of the most influential factors affecting passenger satisfaction (de Oña & de Oña, 2015). Reliability generally refers to the ability of transport services to operate according to planned schedules and provide predictable travel experiences. Delays, service disruptions, and inconsistent waiting times are commonly identified as major sources of passenger dissatisfaction. In urban environments where large numbers of commuters depend on public transport for daily travel, reliability plays a critical role in determining overall service quality. Comfort and overcrowding also represent important dimensions of passenger experience. High passenger density, limited seating availability, and insufficient personal space can negatively affect perceptions of transport quality. Previous research has shown that overcrowding and comfort conditions can significantly influence passengers' perceived service quality and overall

satisfaction (dell’Olio et al., 2011). These issues are particularly relevant in large metropolitan cities where public transport systems frequently operate near capacity during peak periods. Accessibility and transfer convenience constitute additional factors that shape passenger evaluations of transport services. Accessibility refers to the ease with which passengers can reach transport services and complete their journeys, while transfer convenience relates to the efficiency of moving between different transport modes or routes. Poor station accessibility, long transfer distances, and inadequate wayfinding systems may negatively affect passenger experiences even when operational performance remains satisfactory (Nathanail, 2008). In recent years, researchers have increasingly explored alternative approaches to evaluating transport service quality through the analysis of digital data sources. The widespread adoption of online review platforms, social media, and mobile applications has generated large volumes of user-generated content that reflect passenger experiences in real-world contexts (Kaplan & Haenlein, 2010). Unlike traditional surveys, online comments are often produced voluntarily and immediately following travel experiences, providing valuable insights into passenger perceptions. Dou et al. (2024) demonstrated the value of online reviews for understanding passenger perceptions of transport services through a study of the Shanghai metro system. Their research showed that online comments can reveal important concerns relating to delays, overcrowding, service quality, and travel experiences. The study highlights how digital feedback can complement traditional transport evaluation methods and provide a richer understanding of passenger perspectives. The increasing availability of user-generated content has therefore created new opportunities for transport service evaluation. However, the large volume and unstructured nature of online comments present challenges for analysis. Consequently, researchers have increasingly turned to Natural Language Processing techniques to support the extraction of meaningful information from large-scale textual datasets (Aggarwal & Zhai, 2012). These developments provide the foundation for the present study, which seeks to integrate passenger feedback analysis with spatial transport analysis through a geo-located NLP feedback system.

### 2.2 User-Generated Content in Transport Research

The rapid growth of digital technologies and online communication platforms has fundamentally changed how individuals share experiences, opinions, and information. Social media platforms, online review websites, discussion forums, and mobile applications have enabled users to generate and distribute large volumes of content related to products, services, and everyday activities. This information, commonly referred to as User-Generated Content (UGC), has

become an increasingly valuable source of data for researchers seeking to understand public perceptions, behaviours, and experiences (Kaplan & Haenlein, 2010). User-Generated Content refers to any form of content created and shared by users rather than organisations or service providers. Examples include online reviews, social media posts, comments, ratings, photographs, and discussion forum contributions. Unlike traditional survey responses, UGC is often created voluntarily and reflects users' spontaneous reactions to real experiences. Consequently, many researchers argue that UGC can provide insights that are difficult to capture through conventional data collection methods because it represents naturally occurring user opinions rather than researcher-controlled responses (Cheung & Thadani, 2012). The emergence of UGC has created new opportunities for transport research. Traditionally, transport studies relied heavily on surveys, interviews, focus groups, and official complaint records to understand passenger experiences. Although these methods remain valuable, they often require considerable resources and are typically limited to relatively small samples. In contrast, online platforms generate large quantities of transport-related comments on a continuous basis, providing researchers with access to extensive collections of passenger feedback. Recent studies have demonstrated the value of online reviews for evaluating public transport services. Dou et al. (2024) analysed online reviews of the Shanghai metro system and found that passenger comments contained valuable information relating to service quality, overcrowding, delays, accessibility, and travel experiences. Their findings suggest that online reviews can complement traditional service quality assessments by providing a richer understanding of passenger concerns and expectations. One of the major advantages of UGC is its ability to capture passenger experiences in near real-time. Traditional surveys are often conducted periodically and may not reflect rapidly changing transport conditions. Online comments, however, are frequently generated immediately following travel experiences. This allows researchers and transport operators to observe emerging issues more quickly and identify changes in public sentiment over time. The timeliness of digital feedback makes UGC particularly useful for monitoring user experiences and understanding changing public perceptions (Cheung & Thadani, 2012). Another advantage of UGC is its scale. Modern transport systems generate thousands of online comments across multiple digital platforms. Such volumes of data would be difficult to obtain through traditional survey methods. Large datasets also enable researchers to identify patterns that may not be visible within smaller samples. By analysing substantial collections of passenger feedback, researchers can gain a broader understanding of transport service performance and user experiences. Despite these advantages, UGC also presents several challenges. First, online comments are often highly unstructured. Unlike survey responses that follow predefined formats, user

comments may contain informal language, abbreviations, spelling mistakes, emojis, sarcasm, and mixed sentiments. These characteristics make analysis more complex and require specialised analytical techniques. Text mining approaches are therefore required to transform unstructured textual content into meaningful and analysable information (Aggarwal & Zhai, 2012). Second, UGC may not always represent the entire passenger population. Online reviewers are self-selected participants who choose whether or not to share their experiences. As a result, online comments may be influenced by participation bias, where individuals with particularly positive or negative experiences are more likely to contribute feedback. Researchers must therefore interpret findings carefully and recognise the limitations associated with online data sources. Third, the large volume of available comments creates challenges for manual analysis. Reading and interpreting thousands of comments is both time-consuming and impractical. Consequently, automated approaches have become increasingly important for extracting meaningful information from UGC datasets. Natural Language Processing techniques provide effective tools for addressing these challenges by enabling the automated classification, interpretation, and analysis of textual data (Jurafsky & Martin, 2024). As a result, UGC has become an important research resource within transport studies. The increasing availability of online reviews offers opportunities to complement traditional transport evaluation methods and improve understanding of passenger experiences. However, the effective utilisation of these data requires advanced analytical methods capable of processing large volumes of unstructured text. This need has contributed to the growing adoption of Natural Language Processing techniques within transport research, which forms the focus of the next section.

### 2.3 Natural Language Processing in Transport Analysis

#### 2.3.1 Introduction to NLP in Transport Research

Natural Language Processing (NLP) is a branch of artificial intelligence that focuses on enabling computers to understand, interpret, and analyse human language. NLP combines computational techniques and linguistic knowledge to process textual information and extract meaningful patterns from large collections of language data (Jurafsky & Martin, 2024). As digital communication technologies have expanded, large volumes of textual data have become available through social media platforms, online reviews, discussion forums, and customer feedback systems. These developments have increased the importance of NLP as a tool for analysing unstructured text.

Unlike structured data, textual information is often difficult to analyse using conventional statistical methods. User comments frequently contain complex linguistic characteristics, including informal expressions, abbreviations, spelling errors, emojis, and context-dependent meanings. Text mining and NLP techniques provide systematic approaches for processing such data and identifying patterns that would be difficult to detect through manual analysis (Aggarwal & Zhai, 2012). Within transport research, NLP has become increasingly important due to the growing availability of passenger-generated feedback. Transport operators and researchers now have access to large collections of comments relating to service quality, delays, overcrowding, accessibility, and travel experiences. However, manually analysing thousands of comments is both time-consuming and impractical. NLP techniques provide an effective solution by enabling automated processing and analysis of large-scale textual datasets. Recent studies have applied NLP methods to analyse public transport reviews, social media discussions, and customer feedback records. For example, Dou et al. (2024) demonstrated that online passenger reviews can be analysed to identify service-related concerns and understand user perceptions of the Shanghai metro system. These studies show that NLP can help identify recurring transport issues, detect sentiment patterns, classify passenger concerns, and support service evaluation. The application of NLP in transport research generally focuses on several key tasks, including text classification, sentiment analysis, and opinion mining. Together, these techniques enable researchers to understand what passengers discuss, how they perceive transport services, and which issues are most important from a user perspective. Therefore, NLP provides an important methodological foundation for transforming large-scale passenger feedback into structured information that can support further analysis.

#### 2.3.2 Text Classification

Text classification is one of the most widely used tasks in Natural Language Processing. It refers to the process of automatically assigning predefined categories to text documents based on their linguistic features and content (Aggarwal & Zhai, 2012). In transport research, text classification can be used to organise passenger comments into issue categories such as delays, overcrowding, accessibility, safety, service reliability, ticketing, and customer service. Traditional text classification approaches relied heavily on manual coding, where researchers read individual documents and assigned categories based on predefined criteria. Although manual classification can provide accurate annotations, it becomes inefficient when applied to large-scale datasets. As a result, machine learning approaches have become widely adopted for automated text classification tasks.

A typical machine learning-based text classification process involves converting textual information into numerical representations. One commonly used approach is Term Frequency– Inverse Document Frequency (TF-IDF), which evaluates the importance of terms based on their frequency within individual documents and across the entire document collection (Aggarwal & Zhai, 2012). TF-IDF representations allow machine learning algorithms to process textual data by converting words into numerical feature vectors. Several traditional machine learning algorithms have been widely applied to text classification tasks. Logistic Regression is commonly used due to its computational efficiency, interpretability, and effectiveness when handling high-dimensional textual features. Support Vector Machines (SVM) have also demonstrated strong performance in text classification tasks by identifying decision boundaries that maximise separation between different categories, particularly in highdimensional feature spaces (Joachims, 1998). Although recent advances in deep learning have introduced more complex approaches for NLP tasks, traditional machine learning models such as Logistic Regression and SVM remain valuable baseline methods. These models often provide advantages in terms of simplicity, interpretability, lower computational requirements, and effectiveness when working with smaller or domain-specific datasets (Aggarwal & Zhai, 2012). In transport-related studies, text classification enables researchers to identify recurring issues and measure the frequency of different passenger concerns. By transforming large collections of unstructured comments into organised categories, researchers can gain a clearer understanding of common service problems and prioritise areas requiring improvement. Within integrated transport analysis systems, classified textual information can also provide structured inputs for further spatial analysis and visualisation.

#### 2.3.3 Sentiment Analysis

Sentiment analysis is another important application area within Natural Language Processing. It focuses on the automatic identification and extraction of opinions, emotions, and attitudes expressed in textual data. The primary objective of sentiment analysis is to determine whether a piece of text expresses a positive, negative, or neutral opinion towards a particular topic, product, service, or experience (Pang & Lee, 2008). With the rapid expansion of online platforms and user-generated content, sentiment analysis has become an important method for understanding public opinions at large scale. Traditional approaches to analysing opinions often relied on manual interpretation, which required significant time and effort. In contrast, computational sentiment analysis techniques enable researchers to automatically process large collections of textual feedback and identify overall patterns of user perception (Liu, 2012).

In the context of public transport research, sentiment analysis provides an effective method for understanding passenger satisfaction and identifying service-related concerns. Passenger comments frequently contain subjective evaluations of travel experiences, including opinions about waiting time, service reliability, overcrowding, cleanliness, safety, and accessibility. By analysing the sentiment expressed in these comments, researchers can better understand how users perceive different aspects of public transport services. Online transport reviews are particularly suitable for sentiment analysis because they often contain direct descriptions of passenger experiences. Positive comments may indicate satisfaction with service reliability, convenience, or comfort, while negative comments may reveal problems such as delays, congestion, poor information provision, or dissatisfaction with service quality. Dou et al. (2024) demonstrated that analysing online reviews of the Shanghai metro system can provide valuable insights into passenger perceptions and identify important factors affecting user satisfaction. Different computational approaches have been developed for sentiment analysis. Early methods commonly relied on lexicon-based approaches, where sentiment was determined using predefined dictionaries containing positive and negative words. However, these methods often struggled with complex language features such as context, sarcasm, and domain-specific expressions. As a result, machine learning approaches became widely adopted because they allow models to learn sentiment patterns from labelled training examples (Pang & Lee, 2008). Traditional machine learning models, including Logistic Regression and Support Vector Machines, have been widely applied to sentiment classification tasks. These approaches usually involve converting textual data into numerical representations through feature extraction methods such as TF-IDF before applying classification algorithms. Although deep learning models have achieved strong performance in many modern NLP applications, traditional machine learning methods remain useful due to their efficiency, interpretability, and suitability for smaller datasets (Aggarwal & Zhai, 2012). Despite its advantages, sentiment analysis also presents several challenges. User-generated comments may include ambiguous meanings, mixed emotions, informal expressions, and context-dependent opinions. For example, a passenger may provide positive feedback about station cleanliness while simultaneously expressing dissatisfaction with overcrowding. These mixed sentiments create difficulties for simple classification approaches and highlight the importance of careful model evaluation. Overall, sentiment analysis provides a valuable approach for transforming subjective passenger opinions into structured information. When combined with other NLP techniques such as text classification and keyword extraction, sentiment analysis enables researchers to identify not only what issues passengers discuss but also how they feel about those issues. This capability provides an important foundation for integrating textual feedback with spatial analysis in transport research.

#### 2.3.4 Opinion Mining and Keyword Extraction

Opinion mining is a specialised area of Natural Language Processing that focuses on identifying and extracting subjective information, opinions, and attitudes from textual data. While sentiment analysis mainly determines the overall emotional polarity of text, opinion mining aims to provide a more detailed understanding of what specific aspects users discuss and how they evaluate those aspects (Pang & Lee, 2008). Therefore, opinion mining is particularly valuable when analysing complex user-generated content where multiple topics and opinions may appear within the same document. In service-related research, user feedback often contains different aspects of customer experiences rather than a single general opinion. For example, a passenger may express satisfaction with the convenience of a metro line while also complaining about overcrowding during peak hours. Traditional document-level sentiment analysis may classify the overall comment as positive or negative but may fail to capture these more detailed concerns. Aspectbased opinion mining addresses this limitation by identifying specific service attributes mentioned in user comments and analysing opinions associated with those attributes (Liu, 2012). Within public transport research, opinion mining provides opportunities to understand passenger concerns at a more detailed level. Transport-related comments usually involve multiple service dimensions, including reliability, comfort, accessibility, safety, cleanliness, information availability, and transfer convenience. Extracting these topics from large-scale textual datasets allows researchers and transport operators to identify which aspects of public transport services receive the most attention from users. Keyword extraction is closely related to opinion mining because it aims to identify important words or phrases that represent the main themes within textual datasets. Instead of manually reading thousands of comments, automated keyword extraction techniques can highlight frequently discussed topics and provide a structured overview of user concerns. Text mining approaches allow researchers to transform large volumes of unstructured textual data into meaningful representations that support further analysis (Aggarwal & Zhai, 2012). Several approaches have been used for keyword extraction and topic identification. Traditional statistical methods identify important terms based on word frequency or weighting techniques such as Term Frequency–Inverse Document Frequency (TF-IDF). These approaches assume that terms appearing frequently within specific documents but less frequently across the entire dataset may represent important information. Although more advanced methods based on deep learning have emerged, traditional approaches remain widely used because of their simplicity, efficiency, and interpretability (Aggarwal & Zhai, 2012). In transport studies, combining sentiment analysis with opinion mining can provide a more comprehensive understanding of passenger feedback. Sentiment analysis explains whether users feel positively or negatively, while opinion mining identifies the specific issues associated with

those feelings. For example, negative sentiment alone may indicate dissatisfaction, but opinion mining can reveal whether the dissatisfaction relates to delays, overcrowding, station facilities, or service information. Recent research has demonstrated the potential of analysing online transport reviews to identify passenger concerns and service quality factors. Dou et al. (2024) showed that online reviews of the Shanghai metro system contain valuable information about passengers' experiences and perceptions. Such studies indicate that user-generated content can provide insights beyond traditional satisfaction surveys by capturing detailed descriptions of real travel experiences. However, opinion mining and keyword extraction also face several challenges. User-generated content often contains informal expressions, incomplete sentences, slang, and context-dependent meanings. Additionally, the same transport issue may be described using different expressions by different users. These linguistic variations increase the difficulty of accurately extracting meaningful information from large-scale feedback datasets. Overall, opinion mining and keyword extraction extend the capability of NLP-based transport analysis by moving beyond general sentiment identification towards a deeper understanding of specific passenger concerns. When integrated with classification techniques and spatial analysis methods, extracted topics and keywords can support the identification and visualisation of transport issues across different geographic locations.

### 2.4 GIS and Spatial Analysis in Urban Transport

#### 2.4.1 GIS in Transport Studies

Geographic Information Systems (GIS) have become important tools for collecting, managing, analysing, and visualising spatial information. GIS enables researchers to organise geographically referenced data and examine relationships between locations, attributes, and spatial patterns (Longley et al., 2015). As urban systems become increasingly complex, GIS-based approaches have been widely adopted to support urban planning, environmental management, transportation analysis, and decision-making processes. In the field of transport research, GIS provides powerful capabilities for representing and analysing transportation networks. Public transport systems consist of multiple spatial components, including routes, stations, stops, transfer points, and administrative boundaries. By integrating these components within a GIS environment, researchers can better understand the structure and accessibility of transport systems. GIS also supports the analysis of relationships between transport infrastructure and surrounding urban environments. Traditional transport analysis has often focused on operational indicators, such as travel time, passenger volume, and network coverage. While these indicators provide important information about transport performance, they may not fully capture how passengers experience services in

different geographic locations. Combining GIS with user-related data creates opportunities to analyse transport systems from both infrastructure and user perspectives. Spatial visualisation is another important function of GIS in transport studies. Maps provide an intuitive method for presenting complex datasets and identifying geographic patterns that may not be easily observed through tables or statistical summaries. With the development of webbased GIS technologies, interactive mapping systems have further improved the accessibility and communication of transport information. Sobral et al. (2019) highlighted that urban mobility visualisation tools can support the exploration and interpretation of complex transport datasets through interactive interfaces. Therefore, GIS provides an essential foundation for connecting transport-related information with geographic locations. When combined with passenger feedback analysis, GIS can help researchers understand not only what problems exist within a transport system but also where those problems occur.

#### 2.4.2 Spatial Clustering Analysis

Spatial clustering analysis is an important method used to identify geographic concentrations and patterns within spatial datasets. In transport research, clustering techniques can help identify areas where specific transport issues occur more frequently. Instead of only understanding the overall frequency of passenger complaints, spatial clustering enables researchers to investigate whether certain problems are concentrated around particular stations, routes, or districts. One widely used spatial clustering method is Density-Based Spatial Clustering of Applications with Noise (DBSCAN). Unlike traditional clustering approaches such as K-means, DBSCAN does not require researchers to define the number of clusters before analysis. Instead, it identifies clusters based on the density of nearby data points and separates isolated points as noise (Ester et al., 1996). This characteristic makes DBSCAN particularly suitable for urban transport analysis. Transportrelated issues are often unevenly distributed across cities, and problematic areas may form clusters with irregular shapes. For example, negative passenger feedback may concentrate around busy transfer stations or specific urban areas. Density-based clustering methods allow researchers to detect these spatial patterns without assuming predefined geographic boundaries. In the context of passenger feedback analysis, spatial clustering provides additional insights beyond traditional text analysis. NLP techniques can identify common issues discussed by passengers, such as delays or overcrowding. However, spatial clustering enables researchers to understand where these issues are concentrated. This combination allows transport problems to be analysed from both semantic and geographic perspectives.

#### 2.4.3 Spatial Autocorrelation Analysis

Spatial autocorrelation analysis examines whether similar values are geographically clustered or randomly distributed. The basic principle of spatial autocorrelation is that nearby locations may demonstrate similar characteristics due to spatial relationships. In transport studies, spatial autocorrelation can be used to determine whether transport-related problems show significant geographic patterns. Moran's I is one of the most widely used measures for evaluating spatial autocorrelation. It measures whether similar values tend to occur close to each other across geographic space . A positive Moran's I value indicates that similar values are spatially clustered, while a negative value suggests spatial dispersion. Values close to zero generally indicate a random spatial distribution. While global Moran's I provides an overall measurement of spatial patterns, it does not identify specific local areas contributing to those patterns. To address this limitation, Local Indicators of Spatial Association (LISA) were developed to identify local spatial clusters and outliers. LISA analysis can classify areas into different spatial relationship categories, such as high-high clusters, low-low clusters, and spatial outliers. In transport feedback analysis, this approach can help identify locations where negative experiences are geographically concentrated and highlight areas that may require further investigation. By combining spatial autocorrelation methods with NLP-based feedback analysis, researchers can move beyond identifying common passenger concerns and evaluate whether those concerns demonstrate meaningful spatial patterns.

### 2.5 Web-based Visualisation and Smart City Applications

#### 2.5.1 Web-based Data Visualisation

The increasing availability of large-scale urban datasets has created new challenges for data interpretation and communication. Although advanced analytical methods can generate valuable insights from complex datasets, these results may be difficult for users to understand without effective presentation methods. Data visualisation has therefore become an important approach for transforming complex analytical outputs into accessible and interpretable information (Few, 2006). Traditional data presentation methods, such as static reports, tables, and charts, provide useful summaries but often have limitations when dealing with dynamic and multidimensional datasets. In contrast, web-based visualisation systems allow users to interact with data through functions such as filtering, searching, zooming, and selecting specific information. These interactive capabilities enable users to explore datasets more flexibly and gain deeper insights compared with static representations.

Within transport research, web-based visualisation plays an important role because transportation systems involve multiple types of data, including geographic locations, passenger flows, service performance indicators, and user feedback. Presenting these datasets through interactive interfaces can help users identify relationships and patterns that may not be immediately visible through numerical results alone. Interactive dashboards have increasingly been adopted as tools for supporting data exploration and decision-making. Dashboards integrate different types of information, including indicators, charts, tables, and maps, into a single visual environment. Effective dashboard design allows users to monitor important information, identify trends, and compare different aspects of system performance efficiently (Few, 2006). For transport applications, dashboards provide opportunities to combine operational data with passenger-centred information. Instead of only presenting technical performance indicators, interactive platforms can incorporate user experiences and feedback analysis results. This allows transport-related information to be communicated in a more accessible format for researchers, planners, and other stakeholders.

#### 2.5.2 Web GIS and Urban Mobility Visualisation

Web Geographic Information Systems (Web GIS) extend traditional GIS capabilities by enabling spatial information to be accessed, analysed, and visualised through web-based platforms. Unlike desktop GIS software, Web GIS allows users to interact with geographic data without requiring specialised software installations, increasing the accessibility of spatial analysis results. In urban mobility research, Web GIS has become particularly important because transport systems are inherently spatial. Transport networks consist of routes, stations, stops, and service areas that need to be understood within geographic contexts. Interactive maps allow users to explore these spatial relationships more effectively by combining geographic information with additional analytical results. Sobral et al. (2019) explained that visualisation techniques are essential for interpreting data generated by intelligent transportation systems. Large volumes of mobility data can be difficult to analyse directly, but visual interfaces allow users to recognise patterns, identify problems, and support transport-related decision-making. The integration of Web GIS with analytical techniques creates further opportunities for understanding transport systems. For example, spatial visualisation can be combined with results from machine learning or text analysis to present complex information in a more understandable format. This approach enables users to explore both where transport issues occur and what types of problems are associated with different locations. In the context of passenger feedback analysis, Web GIS provides a method for connecting user opinions with physical transport networks. While text analysis can reveal passenger concerns,

spatial visualisation enables these concerns to be represented geographically. This combination creates a more comprehensive perspective for analysing transport service quality.

### 2.6 Research Gap and Chapter Summary

Previous studies have demonstrated that digital technologies and data-driven approaches provide new opportunities for understanding and improving public transport systems. Traditional transport evaluation methods have gradually been complemented by online user-generated content, which provides additional information about passenger experiences, opinions, and service expectations. Online reviews and digital feedback have been shown to contain valuable information about passenger perceptions of public transport quality and can support a more user-centred understanding of transport services (Dou et al., 2024). The increasing availability of user-generated content has encouraged the application of Natural Language Processing (NLP) techniques within transport research. NLP methods enable researchers to process large volumes of unstructured textual data and extract meaningful information, including topics, categories, keywords, and sentiment patterns (Jurafsky & Martin, 2024). Through techniques such as text classification, sentiment analysis, and opinion mining, passenger feedback can be transformed into structured information that supports further analysis. However, although NLP-based approaches provide important insights into passenger concerns, many existing studies primarily focus on analysing textual information itself. These approaches can identify what issues passengers discuss and how users perceive transport services, but they often provide limited understanding of where these issues occur geographically. In public transport systems, spatial context is particularly important because service problems are closely connected to specific locations, routes, stations, and surrounding urban environments. At the same time, Geographic Information Systems (GIS) and spatial analysis techniques have been widely applied in transport studies. GIS-based methods allow researchers to represent transport networks, analyse geographic relationships, and visualise spatial patterns. Interactive visualisation approaches further improve the ability to explore and communicate complex urban mobility information (Sobral et al., 2019). However, traditional GIS-based transport analysis has often focused on physical infrastructure, network characteristics, and spatial distributions rather than directly incorporating passenger-generated opinions. This creates a gap between textual feedback analysis and spatial transport analysis. Existing NLP studies can extract meaningful information from passenger comments, while GIS studies can analyse and visualise transport networks. However, fewer studies have integrated user-generated transport feedback, NLP-based text analysis, geographic information, spatial analysis methods, and interactive visualisation within a unified system. This separation limits the ability to understand transport problems from both user experience and geographic perspectives.

Furthermore, the development of smart cities has increased the need for integrated analytical systems capable of combining different types of urban data. Modern urban computing approaches emphasise the importance of collecting, integrating, and analysing heterogeneous data sources to generate useful knowledge for urban management and decision-making (Zheng et al., 2014). Similarly, smart-city research highlights the value of using digital technologies and data-driven methods to improve the efficiency and quality of urban services (Batty et al., 2012). Based on these research gaps, this project proposes the development of a Geo-located NLP Feedback System for Public Transport. Unlike approaches that analyse passenger comments or transport networks separately, this project aims to integrate user-generated feedback, NLP techniques, GIS-based spatial analysis, and web-based visualisation into a single framework. By linking passenger opinions with geographic transport data, the proposed system seeks to provide a more comprehensive understanding of public transport issues. Overall, this chapter reviewed the key research areas related to the proposed system, including public transport service quality, user-generated content, Natural Language Processing, GIS-based spatial analysis, and web-based smart-city applications. The literature indicates that each of these technologies provides important benefits independently, but their integration remains an important opportunity for improving transport analysis. The following chapters describe the methodology, system design, implementation process, and evaluation of the proposed geo-located feedback analysis system.

## 3 Methodology

### 3.1 Research Design and Overall Approach

This project adopts a design-oriented research methodology to develop a Geo-located NLP Feedback System for Public Transport. The main purpose of the project is to design, implement, and evaluate an integrated analytical system that combines Natural Language Processing (NLP), Geographic Information Systems (GIS), spatial analysis techniques, and web-based visualisation. Rather than focusing only on theoretical analysis, this project aims to create a functional prototype that demonstrates how passenger-generated feedback can be transformed into meaningful geographic insights. The methodology was developed based on the research gap identified in the literature review. Existing transport feedback studies often focus on analysing passenger opinions through textual analysis, while spatial transport studies mainly focus on geographic infrastructure and network characteristics. However, limited attention has been given to integrating these two perspectives into a single analytical framework. Therefore, this project follows an integrated workflow that connects textual feedback analysis with spatial transport analysis.

The overall methodology consists of five main stages: data preparation, NLP processing, spatial data integration, web system development, and system evaluation. Each stage produces outputs that are used as inputs for the following stage, forming a complete data processing pipeline. The first stage involves collecting and preparing the required datasets. Passenger feedback data is prepared as the primary textual data source, while public transport network data provides the geographic foundation for spatial analysis. Data preprocessing is performed to clean textual information, standardise data formats, and prepare datasets for later analysis. The second stage focuses on Natural Language Processing. Machine learning techniques are applied to transform unstructured passenger comments into structured information. Text classification is used to identify different categories of transport-related issues, while sentiment analysis is applied to determine passenger attitudes towards public transport services. These processes enable large volumes of feedback data to be analysed automatically. The third stage involves spatial data integration and analysis. Processed feedback results are connected with geographic information, allowing passenger opinions to be linked with specific transport locations. Spatial analysis techniques are then applied to explore geographic patterns within transport feedback, including identifying areas where negative experiences may be concentrated. The fourth stage focuses on developing an interactive web-based system. The purpose of this stage is to present analysis results through an accessible interface that combines textual information, statistical summaries, and spatial visualisation. Interactive components allow users to explore transport feedback from different perspectives. The final stage involves evaluating different components of the system. NLP models are assessed using machine learning evaluation metrics, while spatial analysis outputs are examined to determine whether meaningful geographic patterns can be identified. The overall system is evaluated based on its ability to integrate different technologies and provide useful insights for transport analysis. The complete workflow of the proposed methodology is shown in Figure 3.1.

### 3.2 System Architecture

The system architecture was designed to connect textual feedback processing, geospatial data preparation, backend data services, and web-based visualisation in a single workflow. Instead of treating these components as separate tasks, the project organises them as a pipeline in which each layer produces data that can be used by the next layer. This design was selected because the research problem itself is not only about classifying text or drawing maps, but about linking passenger comments with transport locations in a way that can be explored through an interactive system.

The implemented system contains four main layers. The first layer is the data and model preparation layer. This layer includes the synthetic public transport feedback templates, the hand-labelled out-of-distribution test set, the ChnSentiCorp sentiment dataset, and the QGIS spatial data prepared by the group. It also includes the training scripts used to build the sentiment and category classification models. The second layer is the backend service layer, implemented with FastAPI. The backend receives text from the frontend, applies station matching and NLP analysis, stores processed records in SQLite, and provides API endpoints for feedback records, sentiment aggregation, hotspot data, GIS layers, and spatial statistics. The third layer is the spatial processing layer. It reads QGIS outputs, converts spatial data to GeoJSON, transforms coordinates for AMap compatibility, and calculates DBSCAN clusters, Moran's I, LISA labels, and district comparison results. The fourth layer is the frontend dashboard layer, implemented with Streamlit and Folium. This layer allows users to submit feedback, initialise demonstration data, filter maps, inspect sentiment results, and explore spatial patterns.

In the current implementation, the backend is located in `Project/backend/`, the frontend is located in `Project/frontend/`, model training scripts are located in `Project/training/`, evaluation scripts are stored in `Project/evaluation/`, and QGIS outputs are stored in `Project/qgis/QGIS/`. This structure was useful for the project because it separated responsibilities clearly. Backend services can be tested independently from the dashboard, while the dashboard can be modified without changing the model code. The model contract is also kept stable, which means that a future model can replace the current lightweight classifier without changing the frontend interface.

The system architecture is shown conceptually in Figure 3.1. Passenger feedback is first submitted through the dashboard or generated through the seed endpoint. The backend analyses the text and stores the structured result. Aggregation services then calculate station-level sentiment summaries and hotspot weights. Spatial services use station coordinates to calculate cluster and autocorrelation results. Finally, the Streamlit dashboard displays these results through charts, maps, tables, and model evaluation panels.

### 3.3 Data Processing Workflow

The data processing workflow begins with raw or generated passenger feedback. In the prototype, feedback can be provided through the Streamlit text input form or generated through the `/api/seed` endpoint. The seed function creates a repeatable set of synthetic commuter comments that cover different station names, transport issue categories, and sentiment labels. This repeatable data generation is important because it allows the system to be demonstrated and tested even when live passenger data is not available.

After feedback text is received, the backend applies station matching. The current station matching method checks whether the feedback contains a known Chinese or English station name from the key Shanghai station list. If a station is found, the system attaches the station name, English name, latitude, and longitude to the result. If no station is found, the system still returns an NLP result, but the record is not used for map heatmap generation because it does not contain a reliable geographic point.

The next step is issue classification and sentiment analysis. The system first applies rule-based keyword matching to identify possible categories and sentiment words. These matched keywords are retained because they help explain the classification result. The system then checks whether the trained machine learning model is available. If the model is available, it predicts the category and sentiment. If the model file is missing, the rule result is used as a fallback. This design avoids system failure and keeps the dashboard usable during model development.

The processed feedback record is then saved in SQLite. Each record contains the original text, station information, coordinates, category, sentiment, confidence, matched keywords, and timestamp. Once stored, the record becomes available to the analytics services. The sentiment aggregation service groups feedback by station and category, counting positive, neutral, and negative records. The hotspot service filters negative records with valid coordinates and calculates a relative weight based on the negative-feedback count at each station.

The spatial analysis workflow uses the same stored records but aggregates them at station level. DBSCAN uses station coordinates and negative feedback counts to identify possible clusters. Moran's I calculates whether station-level negative-feedback rates show global spatial autocorrelation. District comparison assigns stations to the supported districts and compares negative rates. This workflow makes the system dynamic: if new feedback is submitted, the database changes, and the dashboard can refresh the analytical outputs.

### 3.4 NLP Processing Methodology

The NLP processing methodology combines a transparent rule baseline with a lightweight machine learning model. This combination was chosen because the project needed a working prototype that could run reliably while still showing a realistic model development process. A pure machine learning approach would require a larger labelled transport feedback dataset, while a pure rule-based system would not demonstrate model evaluation. The hybrid approach therefore provides a practical balance between reliability and research value.

The rule baseline uses keyword dictionaries for the major transport categories. For example, delay-related feedback is identified through words such as "晚点", "延误", "delay", "late", and "waiting". Crowding feedback is associated with words such as "拥挤", "人多", "挤不上", "crowded", and "packed". Similar keyword groups are defined for cleanliness, safety, noise, and accessibility. The sentiment baseline uses negative and positive keyword lists. Negative keywords are checked first because complaints often contain explicit negative service descriptions. If no negative keyword is found but a positive keyword is present, the sentiment is classified as positive. If neither type of keyword is found, the text is treated as neutral.

The machine learning model is implemented as a split-head model. One head predicts the issue category, and the other predicts sentiment. Both heads use TF-IDF character n-gram features and Logistic Regression. Character n-grams were selected because the feedback data contains Chinese text, English text, mixed-language text, station names, and short informal expressions. Character n-grams can represent local text patterns without relying heavily on word segmentation. Logistic Regression was selected because it is efficient, interpretable at a baseline level, and easy to deploy through a local joblib model file.

The model is assembled into `backend/models/nlp_model.joblib`, and the backend loads it through `services/ml_model.py`. The output of the model is kept compatible with the model contract used by the backend. This contract includes category, sentiment, confidence, station information, and matched keywords. The stability of this contract is important because the frontend depends on these fields. If a future model is introduced, it only needs to provide the same output structure.

### 3.5 Spatial Analysis Methodology

The spatial analysis methodology is based on the idea that passenger feedback becomes more useful when it is linked to locations. A negative comment about crowding becomes more meaningful if it can be placed at a specific station or district. For this reason, the system performs spatial analysis only on feedback records that contain a matched station and valid coordinates.

Three spatial techniques are used. The first technique is heatmap visualisation. Negative feedback points are passed to the frontend with a relative weight. This allows the dashboard to show areas where negative records are more concentrated. The second technique is DBSCAN clustering. DBSCAN identifies groups of nearby stations with negative feedback without requiring the number of clusters to be known in advance. It uses the Haversine metric because the station data is represented as longitude and latitude. The third technique is Moran's I, which is used to test whether negative-feedback rates are spatially autocorrelated across stations. The system also generates LISA labels to support local interpretation.

District comparison is included as an additional spatial method. The current implementation uses approximate bounding boxes to assign stations to Huangpu, Hongkou, or Pudong. This is sufficient for demonstrating the workflow, although a more accurate version should use polygon containment based on official district boundaries. The comparison uses a chi-square test to examine whether negative and non-negative feedback rates differ across districts.

### 3.6 Web-based System Development Methodology

The web-based system was developed as a Streamlit dashboard because Streamlit supports rapid development of research prototypes and integrates well with Python-based data analysis. This was suitable for the project because the main goal was to demonstrate a complete analytical workflow rather than build a production front-end framework. Folium and streamlit-folium were used for map rendering because they support interactive map layers, marker popups, heatmaps, layer controls, and integration with GeoJSON data.

The dashboard was designed around the main tasks that a user may need to perform. These tasks include submitting feedback, checking backend connection status, seeding demonstration records, selecting map layers, viewing metro network data, analysing sentiment distribution, identifying hotspots, exploring spatial clusters, and reviewing model evaluation results. The interface is organised into five main tabs: Metro Network, Sentiment Analysis, Hotspot Detection, Spatial Insights, and Methods & Evaluation.

The dashboard also includes a sidebar for configuration. Users can switch between light and dark themes, select district focus, choose the map tile style, toggle key station markers, toggle QGIS bus stops, and filter metro lines. The sidebar also shows model status and backend connection status. This allows the user to understand whether the system is functioning before interpreting the results.

### 3.7 Evaluation Strategy

The evaluation strategy was designed to assess both the individual components and the integrated system. For the NLP component, three evaluation levels were used. The first was a small hand-labelled baseline evaluation containing 27 public transport cases. The second was the training and testing evaluation of the sentiment and category heads. The third was the out-of-distribution evaluation based on 120 hand-labelled transport feedback texts. The OOD evaluation is treated as the most important result because it tests whether the model can handle expressions outside the training templates.

For the spatial analysis component, evaluation was performed on 420 seeded feedback records. The results include DBSCAN cluster counts, noise station counts, Moran's I statistics, and district comparison outputs. These results do not claim to represent real Shanghai passenger behaviour. Instead, they demonstrate that the spatial methods are implemented correctly and can produce interpretable outputs when feedback data is available.

The integrated system was evaluated by checking whether the backend API, SQLite database, NLP analysis, GIS layer conversion, map rendering, and dashboard interaction work together. This included testing the `/api/health`, `/api/feedback`, `/api/sentiments`, `/api/hotspots`, `/api/spatial/clusters`, `/api/spatial/moran`, and GIS endpoints. The dashboard was also tested by submitting sample feedback, initialising synthetic data, viewing sentiment charts, rendering heatmaps, and checking the sidebar behaviour.

### 3.8 Chapter Summary

This chapter described the methodology used in the project. The project follows a design-oriented approach and develops a working prototype that integrates NLP, GIS, spatial analysis, backend APIs, database storage, and web visualisation. The methodology is structured as a pipeline from feedback text to geographic analysis. The following chapter explains the data sources and preparation steps used to support this workflow.

## 4 Data Collection and Preparation

### 4.1 Overview of Data Used in the Project

The project uses several types of data because the system needs to combine textual feedback with transport geography. The main data sources include synthetic public transport feedback, a hand-labelled out-of-distribution test set, the ChnSentiCorp sentiment dataset, key Shanghai metro station data, metro route data, and QGIS spatial files. Each data source serves a different purpose in the project.

The feedback data is used for NLP processing and system demonstration. The station and route data provide the geographic reference needed to locate feedback on the map. The QGIS files provide additional spatial layers for district boundaries, subway lines, subway stops, and bus stops. The evaluation data is used to measure model performance and spatial analysis outputs. Together, these data sources allow the system to move from text analysis to spatial interpretation.

### 4.2 Public Transport Network Data

The transport network data used by the dashboard is stored in `frontend/shanghai_metro_data.py`. This file contains metro route coordinates, metro line information, and key station metadata. Each key station includes its Chinese name, English name, longitude, latitude, line information, and station type. The station list includes important interchange and landmark stations such as People's Square, Lujiazui, Century Avenue, Xujiahui, Jing'an Temple, Zhongshan Park, Hongqiao Railway Station, and Shanghai Railway Station.

This station dataset is important because it connects text to geography. When the backend identifies a station name in a feedback comment, it uses this station list to attach coordinates. Without this step, the system could still classify the text, but it would not be able to display the feedback on a map or include it in spatial analysis.

Metro route data is used to draw the network on the Folium map. The route coordinates are stored as lists of longitude and latitude pairs, and each metro line is associated with its display colour. The dashboard allows users to filter which lines are visible. This provides context for the feedback points and makes it easier to interpret whether issues are located near important interchange areas.

### 4.3 Feedback Data Preparation

The project currently uses synthetic feedback for the working dashboard. This choice was made because collecting real passenger feedback from online platforms may involve ethical, privacy, and data-access concerns. Synthetic feedback allows the system to be developed and tested in a controlled way while still representing common transport issues.

The synthetic generator is implemented in `backend/services/nlp_baseline.py`. It produces feedback records using templates for negative, positive, and neutral comments. The negative templates cover six issue categories: Delay, Crowding, Cleanliness, Safety, Noise, and Accessibility. Positive templates describe improved or satisfactory service conditions, such as clean stations, punctual trains, safe management, and convenient accessibility. Neutral templates describe normal passenger flow or ordinary station use.

The default seed endpoint generates 420 feedback records. The generation process is deterministic because it uses a fixed random seed. This means the same demonstration data can be reproduced, which is useful for testing and reporting. After the seed data is generated, each text is analysed by the backend and stored in SQLite.

Examples of generated feedback include comments such as "人民广场站今天晚点太严重了", "陆家嘴站很干净", and "Century Avenue is packed during rush hour". These examples are not intended to represent real-world data, but they are useful for testing whether station matching, category classification, sentiment analysis, database storage, and map rendering work as expected.

### 4.4 Out-of-distribution Test Set

To avoid relying only on template-based data, the project also uses a hand-labelled out-of-distribution test set. The file is stored at `data/evaluation/ood_test_set.jsonl` and contains 120 feedback records. Each record includes text, category, sentiment, source, and perturbation type. The data includes Chinese, English, and mixed examples. It also includes typos, synonyms, emojis, hard neutral examples, and expressions that do not exactly match the training templates.

This test set is important because it provides a more realistic measure of model generalisation. In-domain synthetic test results can be misleading because the model may learn template structures. The OOD set makes the task harder by using different wording. For example, instead of saying directly that a train was "delayed", a comment may say that passengers waited for half an hour. Instead of using a standard cleanliness keyword, a comment may describe smell, liquid, or rubbish indirectly.

The OOD set contains examples such as "今早人民广场那边出了点问题，等了半个多小时一辆车都没来，气死人了", labelled as Delay and negative. Another example is "陆家嘴站人太塞了😤，早高峰根本挤不上去", labelled as Crowding and negative with emoji perturbation. These examples help reveal whether the model can handle more natural and less template-like feedback.

### 4.5 Sentiment Training Data

The sentiment model uses ChnSentiCorp together with synthetic transit examples. ChnSentiCorp provides Chinese sentiment data with positive and negative labels. It is not a public transport dataset, but it helps expose the sentiment model to natural Chinese opinion expressions. However, it does not contain a neutral label, which creates a limitation for three-class sentiment analysis. For this reason, neutral transit examples are introduced through synthetic templates.

The sentiment head was trained on 10,217 rows and tested on 1,927 rows. The use of GroupShuffleSplit by template ID helps reduce template-level leakage in the synthetic portion of the data. Even so, the sentiment task remains challenging because positive and negative expressions in general review datasets do not always map perfectly to transport feedback.

### 4.6 QGIS Spatial Data

The GIS component uses QGIS outputs stored in `qgis/QGIS/`. The supported districts are Huangpu, Hongkou, and Pudong. The spatial files include district boundaries, subway line layers, subway stop layers, and bus stop layers. These files were prepared in QGIS and then integrated into the backend through `backend/services/geo_layers.py`.

The backend reads these files using GeoPandas. If the file has a coordinate reference system, it is converted to EPSG:4326. If no coordinate reference system is detected, it is treated as EPSG:4326. After the layer is cleaned, the geometry is transformed to GCJ-02. This transformation is necessary because the dashboard uses AMap tiles, and AMap uses GCJ-02 coordinates. Without the transformation, QGIS points and lines would not align correctly with the map background.

The dashboard can display QGIS district boundaries, subway lines, subway stops, and bus stops. This makes the feedback analysis more spatially meaningful because the user can view passenger concerns together with transport infrastructure.

### 4.7 Data Preparation Limitations

The main limitation of the data preparation process is that the feedback records are not real passenger comments collected from live platforms. This limits the ability to make claims about actual service problems in Shanghai. The purpose of the dataset is therefore system demonstration and methodological validation rather than real operational analysis.

A second limitation is that the QGIS data covers only three districts. Although Huangpu, Hongkou, and Pudong are important urban areas, they do not represent the complete Shanghai transport system. Future work should extend the spatial data coverage and include more station and route layers.

Finally, the station matching approach depends on known station names. If a passenger refers to a location indirectly, uses a nickname, or makes a spelling mistake, the system may fail to attach coordinates. This is an important limitation for future location extraction work.

### 4.8 Chapter Summary

This chapter described the data used in the project and explained how it was prepared for the NLP, GIS, and dashboard components. The project uses synthetic feedback for demonstration, a hand-labelled OOD set for evaluation, ChnSentiCorp for sentiment training, station data for geolocation, and QGIS layers for spatial context. The next chapter discusses the NLP implementation and evaluation results in detail.

## 5 NLP Model Implementation and Evaluation

### 5.1 Implementation Overview

The NLP component is responsible for transforming raw feedback text into structured information. In the implemented system, each feedback record is processed to identify the station, issue category, sentiment label, confidence score, and matched keywords. This output is then stored in the database and used by the dashboard.

The main NLP files are `backend/services/nlp_baseline.py`, `backend/services/ml_model.py`, `training/train_sentiment.py`, `training/train_category.py`, and `training/train_nlp_model.py`. The baseline file contains station matching, keyword rules, sentiment rules, and synthetic feedback generation. The model loader file loads the trained joblib model. The training files build the sentiment head, category head, and assembled model artifact.

### 5.2 Station Matching

Station matching is performed before category and sentiment interpretation. The system checks the feedback text against the key station list. Both Chinese station names and English station names are considered. The stations are sorted by name length so that longer station names are checked first. This helps reduce incorrect partial matching when station names overlap.

If a station is matched, the system attaches the station's Chinese name, English name, latitude, and longitude. If no station is matched, the station fields are returned as null. This is an important design choice because the system should not invent a location when it cannot identify one. Records without matched coordinates can still be stored and analysed textually, but they are excluded from heatmap and spatial clustering outputs.

### 5.3 Category Classification

The category classification task uses seven labels: Delay, Crowding, Cleanliness, Safety, Noise, Accessibility, and Other. These categories were selected because they reflect common public transport issues and can be interpreted by planners or operators. Delay and crowding relate to service reliability and passenger capacity. Cleanliness relates to station and carriage conditions. Safety relates to perceived risk and crowd management. Noise relates to the travel environment. Accessibility relates to elevators, escalators, ramps, wheelchairs, and other facilities.

The rule baseline uses keyword lists for each category. For example, Delay includes words such as "晚点", "延误", "delay", and "late". Crowding includes "拥挤", "人多", "crowded", and "packed". Accessibility includes "电梯", "扶梯", "无障碍", "wheelchair", and "elevator". The classifier counts matched keywords and selects the category with the highest number of matches. If no category keyword is found, the result is Other.

The machine learning category head uses TF-IDF character n-grams and Logistic Regression. The category training data contains 4,365 training rows and 1,170 test rows. In the training evaluation, the category model achieved 1.0000 accuracy and 1.0000 macro-F1. This result needs careful interpretation. It shows that the model fits the synthetic template dataset very well, but it does not prove that the model generalises to real-world feedback. This is why the OOD evaluation is more important.

### 5.4 Sentiment Analysis

The sentiment task uses three labels: positive, neutral, and negative. The rule baseline checks negative keywords first, then positive keywords. If neither is found, the text is treated as neutral. This simple method is easy to explain, but it can make mistakes when keywords appear in a negated or neutral context. For example, a sentence saying that a station is "not crowded" contains a crowding keyword but expresses a positive or neutral experience.

The sentiment model is trained using ChnSentiCorp and synthetic transit examples. The sentiment training set contains 10,217 rows, and the test set contains 1,927 rows. The sentiment model achieved 0.8085 accuracy and 0.5653 macro-F1. The macro-F1 is lower than the accuracy because the neutral class is difficult. The ChnSentiCorp dataset is binary, so neutral examples mainly come from synthetic transit data. This affects the model's ability to recognise subtle neutral feedback.

### 5.5 Model Assembly and Backend Deployment

The project uses `training/train_nlp_model.py` to train and assemble the model. The assembled file is saved as `backend/models/nlp_model.joblib`. This file contains both the category model and the sentiment model. The backend loads the model through `services/ml_model.py`. If the model file is missing, the backend returns to the rule baseline.

This design makes the system robust. The dashboard does not depend on the training process being repeated every time. Once the model artifact exists, the backend can load it and use it for prediction. If future work introduces a BERT-based model or another classifier, the replacement can be made inside the model service while keeping the API fields unchanged.

### 5.6 Baseline Evaluation Results

The rule baseline was first evaluated on a small hand-labelled set of 27 public transport feedback cases. This evaluation is stored in `data/evaluation/baseline_metrics.json`. The category task achieved 0.8889 accuracy and 0.8912 macro-F1. The sentiment task achieved 0.7778 accuracy and 0.7493 macro-F1.

These results show that the rule baseline works reasonably well on simple examples. It performs especially well when issue keywords are explicit. However, the evaluation set is small, and the result should not be treated as a complete measure of real-world performance. The baseline is more useful as a reference point for system integration and interpretability.

<!-- pagebreak -->

### 5.7 Out-of-distribution Evaluation

The main NLP evaluation uses the 120-case OOD test set. Three model variants were compared: the rule baseline, TF-IDF with Logistic Regression, and TF-IDF with LinearSVC. The results are shown in Table 5.1.

| Model | OOD Cat. Acc. | OOD Cat. F1 | OOD Sent. Acc. | OOD Sent. F1 | ChnSent. Acc. | ChnSent. F1 |
|---|---:|---:|---:|---:|---:|---:|
| Rule baseline | 0.5833 | 0.5883 | 0.5417 | 0.4410 | 0.9108 | 0.9108 |
| TF-IDF + LR | 0.5833 | 0.5883 | 0.5417 | 0.4410 | 0.9108 | 0.9108 |
| TF-IDF + SVC | 0.5917 | 0.5929 | 0.5500 | 0.4513 | 0.9342 | 0.9342 |

The OOD results show that the current model has limited generalisation. TF-IDF with Logistic Regression performs the same as the rule baseline on the OOD set. TF-IDF with LinearSVC performs slightly better, but the improvement is small. This suggests that the current machine learning model is still strongly dependent on surface-level patterns and keywords. It has not learned a deep semantic understanding of transport feedback.

This result is not necessarily negative for the project. In fact, it provides an honest finding. It shows that template-generated data can support system development but is not enough for robust NLP generalisation. It also supports the argument that future work should use real labelled public transport comments or stronger language models.

### 5.8 Confusion Matrix Evidence

The evaluation script outputs confusion matrices for the OOD test set. The sentiment confusion matrix is stored at `data/evaluation/ood_confusion_sentiment.png`, and the category confusion matrix is stored at `data/evaluation/ood_confusion_category.png`. These figures are included in the Word version of the report.

The confusion matrices help show where the model makes mistakes. In particular, neutral sentiment is difficult because neutral comments may still contain words related to problems, such as delay, crowding, or construction. Category confusion also occurs when one text contains multiple issues. For example, a station may be crowded because a train was delayed, or an accessibility issue may also create a safety concern. A single-label classifier cannot fully represent this complexity.

### 5.9 NLP Evaluation Discussion

The NLP implementation meets the system requirement because it can classify feedback, return structured outputs, support explanation through matched keywords, and provide evaluation evidence. At the same time, the evaluation shows clear limitations. The strongest evidence is the difference between in-domain category performance and OOD performance. The in-domain category model achieved perfect scores, but the OOD macro-F1 was around 0.59. This indicates that the model fits synthetic templates but does not generalise strongly to new expressions.

For the purposes of this project, the model should therefore be described as a baseline. Its value lies in proving that the system can connect NLP outputs to GIS and dashboard components. The model is good enough for prototype integration, but it should not be used for real operational decision-making without further training and validation.

### 5.10 Chapter Summary

This chapter presented the NLP component of the project. The system uses station matching, rule-based classification, a lightweight machine learning model, and a stable output contract. Evaluation results show that the current model provides a useful baseline but has limited OOD generalisation. The next chapter discusses how the structured NLP outputs are used in spatial analysis.

## 6 Spatial Analysis Implementation

### 6.1 Spatial Processing Overview

The spatial analysis component transforms station-level feedback records into geographic outputs. Once feedback records are linked to station coordinates, they can be mapped, clustered, and compared across areas. This is the main reason the project combines NLP with GIS. NLP provides the meaning of the feedback, while GIS provides the geographic context.

The spatial analysis service is implemented in `backend/services/spatial_analysis.py`. It reads records from SQLite and aggregates them by station. For each station, it counts positive, neutral, and negative feedback. It then calculates negative-feedback intensity and applies spatial analysis methods.

### 6.2 Hotspot Heatmap Generation

The hotspot heatmap is generated from negative feedback records that have matched stations and valid coordinates. The backend calculates the number of negative records for each station and normalises the value by the maximum negative count across stations. This produces a weight between 0 and 1. The frontend passes these weighted points into a Folium HeatMap layer.

The heatmap is useful for visual exploration. It allows users to quickly identify areas with more negative feedback in the demonstration data. However, heatmap results should be interpreted carefully. A station with more feedback may appear more intense not because it is worse, but because it is busier or more frequently mentioned. A future version should normalise by station passenger volume or total feedback volume.

### 6.3 DBSCAN Clustering

DBSCAN is used to identify geographic clusters of negative-feedback stations. The method is suitable because the number of clusters does not need to be specified in advance. The backend uses Haversine distance because the input coordinates are geographic coordinates.

The spatial evaluation was conducted on 420 seeded feedback records. With the default parameters of 1.5 km radius and two minimum samples, DBSCAN identified four clusters and eleven noise stations. The cluster output is stored in `data/evaluation/spatial_clusters.geojson`, and the static cluster map is stored in `data/evaluation/spatial_cluster_map.png`.

The DBSCAN output includes the cluster ID, whether the point is noise, station count, station names, total negative records, total feedback, negative rate, and category filter. These properties allow the dashboard to display cluster information in popups and summary indicators.

The result demonstrates that negative feedback can be grouped spatially. However, because the seeded records are synthetic, the cluster locations are not evidence of real Shanghai transport problems. They should be understood as evidence that the method and system integration work.

### 6.4 Moran's I and Local Spatial Association

Moran's I is used to test whether station-level negative-feedback rates are spatially autocorrelated. The negative-feedback rate is calculated as the number of negative records divided by the total number of records at the station. The system builds a K-nearest-neighbour spatial weights matrix and calculates global Moran's I.

The evaluation result was:

| Metric | Value |
|---|---:|
| Moran's I | -0.1030 |
| Expected I | -0.0370 |
| z-score | -0.2001 |
| p-value | 0.8414 |
| Interpretation | No significant spatial autocorrelation detected |

The result indicates that the seeded feedback data does not show significant global spatial clustering of negative-feedback intensity. This is an important result because it shows that the system is not simply forcing a hotspot interpretation. The method can also report when there is no significant spatial pattern.

The system also calculates LISA labels for local interpretation. In the current output, most stations are labelled as not significant. This is consistent with the global Moran's I result. If future real data produces stronger local patterns, the LISA layer could help identify High-High hotspots or local outliers.

### 6.5 District Comparison

The district comparison function compares negative-feedback rates across Huangpu, Hongkou, and Pudong. The current implementation assigns stations to districts using approximate bounding boxes. It then creates a contingency table for negative and non-negative feedback and applies a chi-square test.

The evaluation result is shown in Table 6.1.

| District | Station Count | Total Feedback | Positive | Neutral | Negative | Negative Rate | Chi-square p-value | Significant |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Huangpu | 6 | 90 | 17 | 13 | 60 | 0.667 | 0.3667 | False |
| Hongkou | 2 | 30 | 6 | 4 | 20 | 0.667 | 0.3667 | False |
| Pudong | 2 | 30 | 2 | 4 | 24 | 0.800 | 0.3667 | False |

Pudong has the highest negative rate in the seeded data, but the chi-square result is not significant. Again, this result should not be interpreted as evidence about actual passenger experiences. It demonstrates the method and shows how district-level comparison could be performed when real feedback data is available.

### 6.6 Spatial Analysis Limitations

The spatial analysis has several limitations. First, the dataset is synthetic, so spatial patterns are artificial. Second, district assignment uses bounding boxes rather than polygon containment. This can cause errors near district boundaries. Third, feedback counts are not normalised by station passenger flow. Busy stations may naturally generate more feedback. Fourth, the analysis is not time-aware. Real transport issues often vary by time of day, weekday, weather, and service disruption events.

Despite these limitations, the spatial analysis component is valuable because it completes the NLP-GIS pipeline. It shows that classified feedback can be transformed into maps, clusters, spatial statistics, and district comparison outputs.

### 6.7 Chapter Summary

This chapter described the spatial analysis implementation. The system generates heatmap points, DBSCAN clusters, Moran's I statistics, LISA labels, and district comparison outputs. The evaluation results show that the methods run successfully, although the seeded data does not support strong real-world spatial conclusions. The next chapter describes the web-based system implementation.

## 7 System Implementation

### 7.1 Backend Implementation

The backend is implemented using FastAPI. The main file is `backend/app.py`. FastAPI was selected because it is lightweight, supports clear endpoint definitions, and works well with Python data processing services. The backend is responsible for receiving feedback, running NLP analysis, saving results, returning aggregation outputs, and serving spatial data.

The backend initialises the SQLite database on startup. It also enables CORS so that the Streamlit frontend can call the API locally. The backend service is normally started with the command `uvicorn app:app --reload --port 8000` from the `Project/backend` directory.

The key endpoints include `/api/health`, `/api/model/status`, `/api/stations`, `/api/feedback`, `/api/sentiments`, `/api/hotspots`, `/api/seed`, `/api/analyse`, `/api/gis/districts`, and the spatial endpoints. These endpoints make the backend the central connection point between the NLP model, database, GIS files, and frontend.

### 7.2 SQLite Storage

The feedback database is stored at `backend/db/feedback.db`. The table contains the original text, station name, English station name, latitude, longitude, category, sentiment, confidence, matched keywords, and timestamp. SQLite was selected because it is simple and reliable for a local prototype. It does not require a separate database server, and it is easy to reset through the seed endpoint.

The database design is intentionally minimal. It is not intended to be a full production database schema. However, it supports the main needs of the project: saving processed feedback, retrieving records, building aggregates, and running spatial analysis on current records.

### 7.3 Frontend Dashboard Implementation

The frontend is implemented in `frontend/app.py` using Streamlit. The dashboard uses `requests` to communicate with the backend. It uses Pandas for local table and chart preparation, Folium for maps, and streamlit-folium to display Folium maps inside Streamlit.

The dashboard has a top navigation area with five tabs. The Metro Network tab shows the metro network, station markers, QGIS layers, and key station table. The Sentiment Analysis tab shows sentiment breakdown charts and station-level negative feedback. The Hotspot Detection tab displays the heatmap and hotspot ranking. The Spatial Insights tab shows DBSCAN, Moran's I, LISA, and district comparison outputs. The Methods & Evaluation tab shows model comparison results, confusion matrices, OOD examples, and live inference.

The dashboard also includes a feedback input form. Users can type a comment such as "人民广场站今天晚点太严重了", submit it, and receive a structured NLP result. The result is saved in the database, and the dashboard can be refreshed to update the maps and charts.

### 7.4 Sidebar Controls

The sidebar provides system controls. It displays the backend connection status and backend URL. It includes buttons for refreshing data and initialising synthetic feedback. It also includes map controls such as district focus, QGIS bus stop toggle, key station toggle, station label toggle, map style selector, and metro line filter.

The model card in the sidebar shows whether the model is available. If the model file exists, the sidebar displays the model version and available metrics. This helps the user understand whether the dashboard is using the trained model or fallback rules.

### 7.5 GIS Layer Rendering

GIS layers are rendered through Folium GeoJson and marker layers. When a user selects a district, the frontend requests district boundary, subway line, subway stop, and bus stop data from the backend. The backend reads QGIS files and returns GeoJSON. The frontend then adds these layers to the map.

This is important because it connects the dashboard to the group's QGIS work. The dashboard is not only showing station points from a Python file. It is also able to display QGIS-prepared spatial layers from the project folder. This makes the system more complete from a GIS perspective.

### 7.6 User Interface Design

The interface was refined to look more professional and simpler. The visual style uses a dark theme, clear spacing, compact cards, and restrained colour. The aim was not to make a decorative landing page, but to make an analytical dashboard that is easy to read during demonstration. The cards show key metrics, while the maps and tables provide detailed exploration.

One practical UI issue was fixed during implementation. In Streamlit, collapsing the sidebar can hide the built-in button used to open it again if custom CSS hides the header or toolbar. The final implementation keeps the sidebar expand and collapse button visible. This improves usability because the user can close and reopen the sidebar without losing access to controls.

### 7.7 Methods and Evaluation Page

The Methods & Evaluation tab is included because the project needs to show evidence, not only visual outputs. This tab displays the model comparison CSV, OOD confusion matrices, live inference, OOD test set samples, and training metrics. It allows the report discussion to be supported by visible outputs in the system itself.

This page also helps demonstrate that the project is not simply a mock dashboard. It shows that there is a model evaluation pipeline behind the interface. During presentation, this page can be used to explain the difference between in-domain results and OOD results.

### 7.8 Running the System

The system can be run locally. The dependencies are installed through `requirements.txt`. The backend is started from `Project/backend` using uvicorn, and the frontend is started from the project root using Streamlit. After opening the dashboard, the user can initialise data from the sidebar and then explore all tabs.

The backend health endpoint returns `{"status": "ok"}` when the API is running. The frontend uses this endpoint to display connection status. If the backend is offline, the frontend shows an error instead of crashing.

### 7.9 System Verification

The system was verified through multiple checks. The frontend Python file was compiled to confirm syntax validity. The backend and frontend were run locally. Browser testing confirmed that the dashboard rendered, the backend connection status appeared, the sidebar could be collapsed and reopened, and the main UI remained usable in dark mode. API outputs were also checked through the dashboard and command-line requests.

These checks do not replace formal automated testing, but they confirm that the prototype is functional and suitable for demonstration.

### 7.10 Chapter Summary

This chapter described the implementation of the backend, database, frontend dashboard, GIS layers, and user interface. The system is a complete working prototype that connects NLP processing, spatial analysis, and web visualisation. The following chapter discusses the main findings and limitations of the project.

## 8 Discussion

### 8.1 Achievement of Project Aim

The project achieved its main aim of developing a geo-located NLP feedback system for public transport. The final system is able to process feedback text, identify transport issue categories, predict sentiment, match station names, store records, generate hotspot data, integrate GIS layers, perform spatial analysis, and present results through a web dashboard. This means the project successfully moved beyond a theoretical proposal and produced a working prototype.

The most important achievement is the integration of different technologies. NLP, GIS, backend APIs, database storage, and dashboard visualisation often appear as separate components in transport analysis projects. In this project, they are connected through a shared workflow. A user can submit text in the frontend and see its effect on the database, maps, charts, and spatial analysis outputs.

### 8.2 Interpretation of NLP Findings

The NLP results show that the system works as a baseline but requires stronger data and models for real-world deployment. The in-domain category result is perfect, but this should not be overemphasised. Since the category data is generated from templates, the model can learn patterns that are very close to the test data. The OOD result is more realistic. On the OOD set, the best category macro-F1 is about 0.5929, and the best sentiment macro-F1 is about 0.4513.

These results suggest that the current classifier is useful for demonstrating the system pipeline but not strong enough for operational decision-making. The fact that TF-IDF with Logistic Regression performs the same as the rule baseline shows that the model has not learned much beyond keyword-based patterns. This is an important finding because it shows the limitation of using synthetic templates for NLP training.

At the same time, the model contract and backend design are useful. They allow a future model to replace the current baseline without changing the frontend. Therefore, the project creates a platform for model improvement even if the current model is limited.

### 8.3 Interpretation of Spatial Findings

The spatial analysis results show that the system can produce meaningful spatial outputs, but the current data does not show significant real-world patterns. DBSCAN found four clusters in the seeded data, which demonstrates that the clustering function works. However, Moran's I was -0.1030 with a p-value of 0.8414, indicating no significant global spatial autocorrelation. District comparison also did not show significant differences.

This outcome is reasonable because the data is synthetic. The seeded records were designed to fill the dashboard with examples, not to reproduce real passenger complaint geography. Therefore, the spatial results should be interpreted as method validation rather than transport evidence. The system can calculate and display spatial statistics, but real conclusions would require real feedback data and more careful normalisation.

### 8.4 Strengths of the Project

One strength of the project is that it produces a complete system rather than an isolated model. The user can interact with the dashboard, submit feedback, view maps, inspect model results, and explore spatial analysis. This improves the practical value of the project.

Another strength is the clear separation between frontend and backend. The Streamlit dashboard calls FastAPI endpoints instead of generating all data locally. This makes the architecture more realistic and easier to extend.

A third strength is the integration of QGIS outputs. The system reads the spatial files prepared by the group and converts them into web map layers. This links the GIS work directly with the dashboard.

A fourth strength is that the evaluation is honest. The report does not only show high in-domain metrics. It also includes OOD results that reveal limitations. This makes the project more credible as a research artefact.

### 8.5 Limitations

The project has several important limitations. The first limitation is the lack of real passenger feedback data. The current feedback records are synthetic or hand-labelled test examples. They are useful for demonstration, but they cannot support real operational conclusions about Shanghai Metro or bus services.

The second limitation is model generalisation. The NLP model is trained mainly on synthetic transport templates and external sentiment data. It struggles with varied expressions, subtle neutral cases, and comments that contain multiple issues.

The third limitation is station matching. Exact string matching can fail when users refer to a station indirectly or use informal names. Real user feedback often contains incomplete location references.

The fourth limitation is spatial precision. District assignment currently uses approximate bounding boxes, and station feedback is not normalised by passenger flow. A real system would need better spatial assignment and exposure correction.

The fifth limitation is interface and deployment scale. Streamlit is suitable for the prototype, but a production dashboard may require stronger frontend engineering, authentication, automated tests, and deployment infrastructure.

### 8.6 Practical Implications

Even with these limitations, the project has practical implications. It shows that user feedback can be converted into a form that is easier for planners to inspect. Instead of reading raw comments manually, the system can group them by station, category, sentiment, and district. This could help transport operators identify where more detailed investigation is needed.

The dashboard also shows how feedback analysis can be communicated visually. Maps, heatmaps, cluster layers, and district cards are easier to interpret than raw text files. This is useful for decision-making contexts where different stakeholders need to understand the same information.

The project also shows that evaluation needs to be realistic. If only in-domain synthetic results are reported, the model may appear stronger than it is. The OOD test set gives a more honest view of performance and helps guide future improvement.

### 8.7 Future Work

Future work should first focus on collecting and labelling real public transport feedback. Real feedback would allow the model to learn more natural expressions and would make spatial results more meaningful. The dataset should include different districts, time periods, transport modes, and issue types.

Second, the NLP model should be improved. A transformer-based model such as BERT or RoBERTa could be tested. Multi-label classification should also be considered because many feedback comments mention more than one issue. A future model should also handle typos, synonyms, emojis, and mixed Chinese-English comments more effectively.

Third, the spatial analysis should be improved. District assignment should use polygon containment rather than bounding boxes. Feedback should be normalised by passenger volume or total station feedback. Time-based analysis could be added to identify peak-hour issues or temporary disruptions.

Fourth, the system could be improved as a software product. Docker Compose could make deployment easier. Automated tests could check API behaviour and dashboard outputs. Authentication could be added if the system were used with sensitive feedback data. A more advanced frontend could be developed if more complex user interaction is required.

### 8.8 Research Questions Revisited

The research questions introduced in Chapter 1 can be revisited based on the completed prototype and the evaluation results. The first research question asked what transport-related issues are most frequently discussed by metro and bus users in Shanghai. Because the implemented dataset is mainly synthetic rather than a real online feedback corpus, the project cannot provide a reliable empirical answer about actual Shanghai passengers. However, the system demonstrates how this question could be answered once real comments are available. The classification framework is able to organise comments into delay, crowding, cleanliness, safety, noise, accessibility, and other categories. In the current prototype, these categories are represented in the seeded data so that the dashboard can show how issue frequencies would be calculated and visualised. Therefore, the project answers the question methodologically rather than empirically. It provides the tool and workflow needed to analyse issue frequency, but it does not claim that the synthetic frequencies represent real passenger behaviour.

The second research question asked where these issues are geographically concentrated across the public transport network. The project addresses this question through station matching, coordinate attachment, heatmap visualisation, DBSCAN clustering, Moran's I, and district comparison. The system can identify where negative feedback records are located when a station is matched. The dashboard can display complaint intensity through heatmaps and station bubbles. DBSCAN can group nearby stations with negative feedback, while Moran's I can test whether negative-feedback rates are spatially autocorrelated. In the seeded evaluation, DBSCAN produced four clusters, but Moran's I was not statistically significant. This means that the demonstration data did not show a strong global spatial pattern. The answer to the research question is therefore cautious: the system is capable of identifying geographic concentration, but the current synthetic data does not support a claim about real concentrations.

The third research question asked how NLP and GIS technologies can be integrated to improve the interpretation and visualisation of transport-related user feedback. This question is the strongest part of the project. The implemented architecture shows a clear integration path. NLP extracts structured meaning from text, including station, category, sentiment, confidence, and matched keywords. GIS provides the spatial context through station coordinates, QGIS layers, district boundaries, subway stops, subway lines, and bus stops. The backend connects these layers through API endpoints, and the frontend presents the outputs in interactive maps and charts. This integration improves interpretation because users can see both what kind of issue is being discussed and where it appears in the transport network.

The fourth research question asked to what extent an interactive web-based system can support the exploration and understanding of public transport issues. The dashboard provides evidence that an interactive system can make the analysis more accessible. Users can submit feedback, initialise data, filter metro lines, select district layers, view heatmaps, inspect sentiment distributions, and examine model evaluation results. This is more useful than a static table because it allows users to move between text-level results, station-level results, and spatial-level results. However, the current system remains a research prototype. It supports exploration and demonstration, but it is not yet a professional transport management platform. Its usefulness would increase if connected to real feedback streams, passenger volume data, and a larger GIS database.

### 8.9 Lessons Learned from Prototype Implementation

The implementation process revealed several lessons that are relevant to future projects combining NLP and GIS. The first lesson is that system integration is often as difficult as model development. Building a classifier is only one part of the project. The model output must be stored, aggregated, converted into map-ready formats, and displayed in a way that users can understand. A model that produces category and sentiment labels is not very useful unless those labels can be connected with stations, coordinates, and dashboard components. This is why the project placed emphasis on the API contract and backend services.

The second lesson is that simple baselines are valuable. The rule baseline is not sophisticated, but it helped make the system reliable. It allowed the backend to analyse feedback even before the machine learning model was fully trained. It also provided matched keywords, which helped explain classification decisions. In a research project with limited time, this kind of baseline is useful because it provides a functioning reference point. It also makes it easier to identify whether a machine learning model is genuinely improving on simple keyword logic.

The third lesson is that synthetic data is useful but risky. Synthetic templates made it possible to build and test the dashboard without collecting real passenger comments. They also ensured that all categories were represented. However, the OOD evaluation showed that template data can make a model appear stronger than it actually is. This is an important methodological issue. If the project only reported in-domain scores, it would give an overly positive impression. The OOD test set made the evaluation more realistic and revealed the need for better training data.

The fourth lesson is that spatial analysis needs careful interpretation. A heatmap can look convincing even when the underlying data is synthetic or biased. A cluster can be produced by an algorithm, but that does not automatically mean the cluster represents a real transport problem. For this reason, the report interprets spatial outputs carefully. DBSCAN, Moran's I, and district comparison are presented as implemented methods and demonstration results rather than evidence of actual service conditions.

The fifth lesson is that dashboard usability affects the credibility of the prototype. A system may have correct backend logic, but if the interface is confusing or visually broken, it becomes harder to demonstrate. The sidebar issue in Streamlit was a good example. When the sidebar could not be reopened after being collapsed, the interface became less reliable. Fixing this problem improved the practical quality of the artefact. Small user interface details therefore matter, especially in a project that must be demonstrated to an audience.

### 8.10 Implications for the Final Project Demonstration

The final system can be demonstrated in a structured sequence. First, the presenter can explain the research gap: transport feedback is textual, while transport planning often needs spatial evidence. Second, the dashboard can be opened to show the backend connection and model status. Third, the presenter can submit a sample comment, such as "人民广场站今天晚点太严重了", and show that the system identifies the station, category, sentiment, confidence score, and matched keywords. This provides a direct example of the NLP pipeline.

After the live inference example, the presenter can initialise the seeded data and move to the Sentiment Analysis tab. This tab can be used to explain how individual feedback records become aggregated station and category statistics. The Hotspot Detection tab can then be used to show how negative feedback becomes a heatmap. This helps the audience understand the link between sentiment analysis and spatial visualisation.

The Spatial Insights tab should be used to explain the GIS contribution. The presenter can show DBSCAN clusters, Moran's I values, and district comparison cards. It is important to state clearly that the data is synthetic and that the spatial results demonstrate the method rather than real passenger patterns. This honest interpretation is likely to be stronger than overstating the results.

The Methods & Evaluation tab should be used near the end of the demonstration. It shows that the project includes evaluation evidence, not only a visual interface. The model comparison table and confusion matrices can be used to explain that the current model is a baseline. The presenter can highlight that OOD performance is modest and that this motivates future work with real labelled data and stronger models. This makes the project appear more research-aware and less like a simple dashboard exercise.

### 8.11 Chapter Summary

This chapter discussed the findings, strengths, limitations, and future work of the project. The system successfully demonstrates the integration of NLP and GIS for public transport feedback analysis. However, the results also show that stronger data and models are needed before the system can support real operational decisions.

## 9 Conclusion

This project developed a Geo-located NLP Feedback System for Public Transport using Shanghai as a case-study city. The system integrates passenger feedback analysis, station matching, NLP classification, sentiment analysis, GIS layer processing, spatial analysis, backend APIs, database storage, and web-based visualisation. The final prototype is implemented as a Streamlit dashboard connected to a FastAPI backend.

The project demonstrates that unstructured transport feedback can be transformed into structured information. A feedback text can be analysed to identify a station, category, sentiment, confidence score, and matched keywords. Once stored in the database, these outputs can be aggregated into station-level statistics, heatmaps, hotspot rankings, spatial clusters, Moran's I results, and district comparison tables.

The NLP evaluation shows that the current model is useful as a baseline but limited in real-world generalisation. The OOD results are modest, especially for sentiment macro-F1. This reflects the limitations of synthetic training data and keyword-dependent approaches. However, the system design allows future models to replace the current baseline through the same API contract.

The spatial analysis evaluation shows that the system can perform DBSCAN clustering, Moran's I analysis, LISA labelling, and district comparison. The seeded data did not show significant spatial autocorrelation, but this is an honest and expected result for demonstration data. The value of the spatial component is that it proves the feedback-to-map pipeline works.

Overall, the project provides a practical research prototype that connects NLP and GIS in the context of public transport service analysis. It contributes a working system architecture, an interpretable baseline, a replaceable model interface, QGIS integration, spatial analytics, and dashboard-based visualisation. With real passenger feedback data, stronger NLP models, and expanded GIS coverage, the system could be developed further into a more robust decision-support tool for public transport planning and smart-city applications.

## References

Aggarwal, C. C., & Zhai, C. (2012). Mining Text Data. Springer. https://doi.org/10.1007/978-1-4614-3223-4

Anselin, L. (1995). Local indicators of spatial association: LISA. Geographical Analysis, 27(2), 93-115.

Batty, M., Axhausen, K. W., Giannotti, F., Pozdnoukhov, A., Bazzani, A., Wachowicz, M., Ouzounis, G., & Portugali, Y. (2012). Smart cities of the future. The European Physical Journal Special Topics, 214, 481-518. https://doi.org/10.1140/epjst/e2012-01703-3

Cheung, C. M. K., & Thadani, D. R. (2012). The impact of electronic word-of-mouth communication: A literature analysis and integrative model. Decision Support Systems, 54(1), 461-470. https://doi.org/10.1016/j.dss.2012.06.008

de Oña, J., & de Oña, R. (2015). Quality of service in public transport based on customer satisfaction surveys: A review and assessment of methodological approaches. Transportation Science, 49(3), 605-622. https://doi.org/10.1287/trsc.2014.0544

Dou, M., Gu, Y., & Gong, J. (2024). How do people perceive the quality of urban transport service? New insights from online reviews of Shanghai metro system. Journal of Urban Management, 13(4), 705-719. https://doi.org/10.1016/j.jum.2024.07.008

Eboli, L., & Mazzulla, G. (2007). Service quality attributes affecting customer satisfaction for bus transit. Journal of Public Transportation, 10(3), 21-34. https://doi.org/10.5038/2375-0901.10.3.2

Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. Proceedings of the Second International Conference on Knowledge Discovery and Data Mining, 226-231.

Few, S. (2006). Information Dashboard Design: The Effective Visual Communication of Data. O'Reilly Media.

Goodchild, M. F. (2007). Citizens as sensors: The world of volunteered geography. GeoJournal, 69, 211-221.

Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition (3rd ed. draft). Stanford University. https://web.stanford.edu/~jurafsky/slp3/

Kaplan, A. M., & Haenlein, M. (2010). Users of the world, unite! The challenges and opportunities of social media. Business Horizons, 53(1), 59-68. https://doi.org/10.1016/j.bushor.2009.09.003

Liu, B. (2012). Sentiment Analysis and Opinion Mining. Morgan & Claypool Publishers. https://doi.org/10.2200/S00416ED1V01Y201204HLT016

Longley, P. A., Goodchild, M. F., Maguire, D. J., & Rhind, D. W. (2015). Geographic Information Science and Systems (4th ed.). Wiley.

Moran, P. A. P. (1950). Notes on continuous stochastic phenomena. Biometrika, 37(1/2), 17-23.

Nathanail, E. (2008). Measuring the quality of service for passengers on the Hellenic railways. Transportation Research Part A: Policy and Practice, 42(1), 48-66. https://doi.org/10.1016/j.tra.2007.06.006

Pang, B., & Lee, L. (2008). Opinion mining and sentiment analysis. Foundations and Trends in Information Retrieval, 2(1-2), 1-135. https://doi.org/10.1561/1500000011

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.

Sobral, T., Galvão, T., & Borges, J. (2019). Visualization of urban mobility data from intelligent transportation systems. Sensors, 19(2), 332. https://doi.org/10.3390/s19020332

Zheng, Y., Capra, L., Wolfson, O., & Yang, H. (2014). Urban computing: Concepts, methodologies, and applications. ACM Transactions on Intelligent Systems and Technology, 5(3), Article 38. https://doi.org/10.1145/2629592

## Appendix A Project Evidence Files

The following files are used as evidence for the implementation and evaluation of the project.

| Evidence Area | File |
|---|---|
| Frontend dashboard | `Project/frontend/app.py` |
| Backend API | `Project/backend/app.py` |
| API schemas | `Project/backend/schemas.py` |
| NLP baseline | `Project/backend/services/nlp_baseline.py` |
| Model loading | `Project/backend/services/ml_model.py` |
| SQLite storage | `Project/backend/services/feedback_store.py` |
| Analytics service | `Project/backend/services/analytics.py` |
| GIS layer conversion | `Project/backend/services/geo_layers.py` |
| Spatial analysis | `Project/backend/services/spatial_analysis.py` |
| Model training | `Project/training/train_nlp_model.py` |
| Model comparison | `Project/data/evaluation/model_comparison.csv` |
| OOD sentiment matrix | `Project/data/evaluation/ood_confusion_sentiment.png` |
| OOD category matrix | `Project/data/evaluation/ood_confusion_category.png` |
| Spatial cluster map | `Project/data/evaluation/spatial_cluster_map.png` |

## Appendix B Main Run Commands

The backend can be started using:

```bash
cd /Users/danielyang/Study/158888/Project/backend
uvicorn app:app --reload --port 8000
```

The frontend can be started using:

```bash
cd /Users/danielyang/Study/158888
streamlit run Project/frontend/app.py --server.port 8502
```

The NLP model can be trained using:

```bash
cd /Users/danielyang/Study/158888/Project
python3 training/train_nlp_model.py
```

The model and spatial evaluations can be run using:

```bash
cd /Users/danielyang/Study/158888/Project
python3 evaluation/evaluate_models.py
python3 evaluation/evaluate_spatial.py
```
