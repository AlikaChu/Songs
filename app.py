import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
# import bar_chart_race as bcr


with st.echo(code_location='below'):
    st.title("Работа о песнях. Посмотрим статистику, поищем закономерности.")

    df = pd.read_csv('billboard_top_100_copy.csv')
    
    st.title('Top 100 songs of 2020 (weekly)')
    
    week = st.sidebar.slider("Pick a week", 1, 52)

    st.write("В таблице ниже вы можете увидеть топ-100 треков по данным Billboard за любую неделю 2020 года. "
             "Для выбора недели воспользуйтесь слайдером слева.")

    df_week = df.loc[df['week'] == week]
    st.write("Date: " + df_week.iloc[0]['date'])
    st.dataframe(df_week[['rank', 'artist', 'song']])


    sptf_df = pd.read_csv('regional-global-weekly-2020_2.csv')
    sptf_short = sptf_df[["Streams", "date"]]
    sptf_short["Track Name - Artist"] = (sptf_df["Track Name"].astype(str)
                                         + " - " +
                                         sptf_df["Artist"].astype(str))

    spotify_df = sptf_short.pivot_table(values='Streams', index=['date'], columns='Track Name - Artist')
    spotify_df.fillna(0, inplace=True)
    spotify_df.sort_values(list(spotify_df.columns), inplace=True)
    spotify_df = spotify_df.sort_index()

    # Этот код создаёт видео-анимацию. Лично у меня комп создавал её полчаса. Для того, чтобы создать эту анимацию, нужно отдельное приложение ffmpeg, который не подключается через requirements, поэтому ниже в комментариях прилагаю код, который я использовала, чтобы сделать анимацию. Если у Вас на компьютере установлен ffmpeg, можете запустить этот код у себя и проверить, что он действительно генерирует эту анимацию.
    # bcr.bar_chart_race(df=spotify_df,
    #                     n_bars=10,
    #                     sort='desc',
    #                     title='Most streamed songs of 2020',
    #                     filename='running_bars.mp4',
    #                     steps_per_period=100,
    #                     period_length=1000)
    st.write("Ниже вы можете наблюдать анимацию: это понедельный топ из 10 песен-лидеров по количеству стримов в Spotify. "
             "А ещё они двигаются...")
    st.video("running_bars.mp4")

    source = pd.read_csv("billboard_top_100_year_2020.csv", delimiter=',')


    st.write("К сожалению, Spotify не создаёт общего чарта топ-100 песен года, "
             "поэтому далее я использую данные Billboard Hot 100 2020. "
             "Мне захотелось узнать, есть ли зависимость между длиной трека и его позицией в чарте. "
             "Billboard составляет свой чарт не только по данным Airplay от радиостанций, "
             "но и по стримингу в самых популярных сервисах (вроде Spotify или AppleMusic)."
             "Можно было предположить, что длинные треки могут оказаться менее прослушиваемыми, чем короткие."
             "Однако, как видно из графика ниже, никакой зависимости не наблюдается. "
             "На этом графике по горизонтали идёт измерение длины песен в секундах, "
             "а по вертикали указаны их позиции (от 1 до 100). "
             "Также, если навести курсор на кружочек-песню, можно увидеть её позицию в чарте, название, исполнителя и длину.")
    fig = alt.Chart(source).mark_circle(size=60).encode(
        x='Length (seconds)',
        y=alt.Y('Rank', sort="descending"),
        tooltip=['artist', 'song', 'genres', 'Length (seconds)']
    ).interactive()
    st.altair_chart(fig, use_container_width=True)
