# projectpython.py
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Quan Ly Diem Sinh Vien", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #1E3A8A;'>QUẢN LÝ ĐIỂM SINH VIÊN</h1>",
    unsafe_allow_html=True,
)
st.write("---")

data = {
    "Họ và tên": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Lê Hoàng Chi",
        "Phạm Đức Dũng",
        "Hoàng Thị Hà",
        "Vũ Thị Lan",
        "Đỗ Minh",
        "Bùi Văn Nam",
        "Ngô Hồng Phúc",
        "Phan Thu Trang",
    ],
    "Chuyên cần": [8.0, 9.0, 7.5, 8.5, 6.0, 9.5, 7.0, 8.0, 9.0, 8.5],
    "Giữa kỳ": [7.0, 8.5, 6.5, 9.0, 5.5, 8.0, 7.5, 6.0, 8.5, 9.0],
    "Cuối kỳ": [7.5, 8.0, 7.0, 8.5, 5.0, 9.0, 6.5, 7.5, 8.5, 8.0],
}

df = pd.DataFrame(data)

df["Tong_ket"] = (
    0.2 * df["Chuyên cần"] + 0.3 * df["Giữa kỳ"] + 0.5 * df["Cuối kỳ"]
).round(2)


def xep_loai(score):
  if score >= 8.5:
    return "Giỏi"
  elif score >= 7.0:
    return "Khá"
  elif score >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

dtb_lop = df["Tong_ket"].mean()
max_sv = df.loc[df["Tong_ket"].idxmax()]
min_sv = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = len(df[df["Tong_ket"] >= 5.0])

st.subheader("Bảng Điểm Chi Tiết")
st.dataframe(df, use_container_width=True)

st.markdown("<h3>Thống Kê Tổng Quan</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric(label="Điểm TB Lớp", value=f"{dtb_lop:.2f}")

with col2:
  st.metric(
      label="SV Cao Điểm Nhất",
      value=f"{max_sv['Họ và tên']}",
      delta=f"{max_sv['Tong_ket']}",
  )

with col3:
  st.metric(
      label="SV Thấp Điểm Nhất",
      value=f"{min_sv['Họ và tên']}",
      delta=f"- {min_sv['Tong_ket']}",
      delta_color="inverse",
  )

with col4:
  st.metric(label="Số SV Đạt (>= 5.0)", value=f"{so_sv_dat}/{len(df)}")

st.write("---")

st.subheader("Tra Cứu Thông Tin Sinh Viên")
selected_student = st.selectbox(
    "Chọn tên sinh viên để xem chi tiết:", df["Họ và tên"].tolist()
)

if selected_student:
  student_info = df[df["Họ và tên"] == selected_student].iloc[0]
  c1, c2, c3, c4, c5 = st.columns(5)
  c1.metric("Chuyên cần", student_info["Chuyên cần"])
  c2.metric("Giữa kỳ", student_info["Giữa kỳ"])
  c3.metric("Cuối kỳ", student_info["Cuối kỳ"])
  c4.metric("Tổng kết", student_info["Tong_ket"])
  c5.metric("Xếp loại", student_info["Xep_loai"])

st.write("---")

st.subheader("Biểu Đồ Thể Hiện Điểm Tổng Kết")
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(
    df["Họ và tên"], df["Tong_ket"], color="#3B82F6", edgecolor="#1E3A8A"
)

ax.set_xlabel("Điểm Tổng Kết", fontsize=12, fontweight="bold")
ax.set_ylabel("Họ và Tên Sinh Viên", fontsize=12, fontweight="bold")
ax.set_title(
    "Biểu đồ điểm tổng kết", fontsize=14, fontweight="bold", color="#1E3A8A"
)
ax.set_xlim(0, 10)
ax.grid(axis="x", linestyle="--", alpha=0.7)

for bar in bars:
  width = bar.get_width()
  ax.text(
      width + 0.1,
      bar.get_y() + bar.get_height() / 2,
      f"{width:.2f}",
      va="center",
      ha="left",
      fontsize=10,
      fontweight="bold",
  )

st.pyplot(fig)
plt.close(fig)

st.write("---")

st.markdown(
    "<p style='text-align: center; color: gray; font-size: 13px;'>"
    "Người thực hiện: Đinh Công Quỳnh - MSSV:054208001680"
    "</p>",
    unsafe_allow_html=True,
)
