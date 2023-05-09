import streamlit as st
from st_pages import show_pages_from_config, add_page_title

show_pages_from_config()

st.success("Tüm interaktif uygulamalar [SeisKit](https://seiskit.streamlit.app/) sitesinde bulunabilir.", icon="✅")

with st.sidebar:
    st.info("Tüm veriler 10.02.2023 tarihinde AFAD veritabanından ham olarak elde edilmiştir. \
    Bu aracın herhangi bir ticari amacı olmayıp, araştırmacılar ve mühendisler için bilgi amaçlı oluşturulmuştur.", icon="ℹ️")
    st.info("Güncel veriler icin AFAD sitesini takip ediniz.", icon="⚠️")
    st.markdown("**Katkıda Bulunanlar**")
    st.markdown("[Doğukan Karataş](https://www.linkedin.com/in/dogukankaratas/)")
    st.markdown("[Yunus Emre Daşdan](https://www.linkedin.com/in/yunus-emre-dasdan/)")
    st.markdown("[Dr. Ahmet Anıl Dindar](https://www.linkedin.com/in/adindar/)")
    st.markdown("**Referans**")
    st.markdown("[Doğukan Karataş, 2023, Development of Ground Motion Selection and Scaling Framework Compatible with TBEC-2018 (Under Review),\
                 Earthquake and Structural Engineering MSc Dissertation](https://github.com/dogukankaratas/scalepy/blob/main/Development%20of%20Ground%20Motion%20Selection%20and%20Scaling%20Framework%20Compatible%20with%20TBEC-2018%20(Under%20Review).pdf)")

st.markdown("# Kahramanmaraş Deprem Verilerinin İncelenmesi")
st.markdown("Bu açık kaynak projesinde 6 Şubat tarihinde Pazarcık ve \
Elbistan'da meydana gelen Mw7.7 ve Mw7.6 büyüklüğündeki depremlerin \
AFAD tarafından 10.02.2023 tarihinde yayınlanan verileri incelendi.")

st.image("assets/afadImage.png", width=800)

st.markdown("### Kullanım")
st.markdown('Veri analizlerini görebilmek için menüden Deprem Veri Analizi kısmına tıklayın.')
st.image("assets/guide1.png", width=800)
st.markdown("İlk sekmeyi kullanarak konum bilgileri ile yatay ve düşey elastik tepki \
spektrumlarını elde edebilirsiniz. Ayrıca konuma ait deprem parametlerini görebilir, \
elde ettiğiniz spektrumları csv formatında inderebilirsiniz.")
st.image("assets/guide2.png", width=800)
st.markdown("İkinci sekmeyi kullanarak, Pazarcık'ta gerçekleşen Mw7.7 büyüklüğündeki \
depremin ivme değerlerini görselleştirebilir, o noktadaki hedef spektrumlarla ivme \
değerlerini aynı grafik üzerinde görebilirsiniz.")
st.image("assets/guide3.png", width=800)
st.markdown("Üçüncü sekmeyi kullanarak, Elbistan'da gerçekleşen Mw7.6 büyüklüğündeki \
depremin ivme değerlerini görselleştirebilir, o noktadaki hedef spektrumlarla ivme \
değerlerini aynı grafik üzerinde görebilirsiniz.")
st.image("assets/guide4.png", width=800)

