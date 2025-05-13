# ÁP DỤNG CÁC THUẬT TOÁN AI - SEARCH VÀO 8-PLUZZLE
Dự án này triển khai các thuật toán tìm kiếm Trí tuệ nhân tạo để giải bài toán 8 puzzle. Các thuật toán bao gồm: Tìm kiếm không có thông tin, Tìm kiếm có thông tin, Tìm kiếm cục bộ, Tìm kiếm trong môi trường phức tạp, Bài toán ràng buộc (CSPs) và Học tăng cường (đang phát triển). Dự án cung cấp hình ảnh trực quan (GIF) và biểu đồ hiệu suất để minh họa hoạt động của các thuật toán trong môi trường tĩnh và xác định của bài toán 8 puzzle.
# CẤU TRÚC FOLDER 
__pycache__: Thư mục chứa các file bộ nhớ đệm của Python (tự động tạo).
**ui**: Xây dựng giao diện đồ họa cho ứng dụng giải bài toán 8 puzzle.
**Puzzle**: Mô phỏng một trạng thái của trò chơi.
**main**: Để khởi chạy trò chơi
**Còn lại là các file chứa các code của từng thuật toán**

# Tổng quan về bài toán 8 puzzle
Bài toán 8 puzzle là một trò chơi trượt số trên lưới 3x3, gồm 8 ô số (từ 1 đến 8) và 1 ô trống. Mục tiêu là di chuyển các ô số từ trạng thái ban đầu đến trạng thái mục tiêu (thường là 1-2-3, 4-5-6, 7-8-trống) bằng cách trượt ô trống lên, xuống, trái, hoặc phải.

# Không gian trạng thái 
Tổng số hoán vị có thể có của 9 ô là 9! = 362,880 trạng thái. Tuy nhiên, chỉ có một nửa trong số đó là có thể giải được (gọi là trạng thái hợp lệ hay có thể đạt được). Số không hợp lệ là do vi phạm vị trí tính chất chẵn lẻ của hoán vị.
Mỗi trạng thái có tối đa 4 hành động (di chuyển ô trống), dẫn đến một đồ thị trạng thái với độ sâu tối đa khoảng 31 bước trong trường hợp xấu nhất.

# Độ phức tạp 
Thời gian cần thiết để các thuật toán tìm kiếm giải bài toán có thể khác nhau đáng kể. Đối với các thuật toán tìm kiếm mù (không sử dụng thông tin heuristic), độ phức tạp thời gian có thể lên đến O(b^d), với b là hệ số rẽ nhánh (số lượng các trạng thái con có thể từ một trạng thái) và d là độ sâu của cây tìm kiếm. Ngược lại, các thuật toán heuristic tối ưu có thể đạt độ phức tạp thời gian tốt hơn, chẳng hạn như O(n).
Tương tự, yêu cầu về bộ nhớ (độ phức tạp không gian) cũng thay đổi. Các thuật toán tiết kiệm bộ nhớ chỉ cần O(d) bộ nhớ, trong khi các thuật toán lưu trữ toàn bộ các trạng thái đã xét có thể cần tới O(b^d) bộ nhớ.

# Tính chất
Tĩnh: Trạng thái của bài toán không thay đổi trong khi tìm kiếm giải pháp.
Xác định: Mỗi hành động (di chuyển ô trống) luôn cho một kết quả duy nhất.
Rời rạc: Số lượng trạng thái và hành động có thể là hữu hạn.
Tính khả thi có hạn: Không phải mọi trạng thái ban đầu đều có thể biến đổi thành mọi trạng thái đích; điều này phụ thuộc vào tính chẵn lẻ của các hoán vị trong bàn cờ.

# Tìm kiếm không có thông tin (Uninformed Search)
Uninformed Search bao gồm các thuật toán như BFS, DFS, UCS, và IDDFS. Dưới đây là các hình ảnh trực quan cho từng thuật toán, cùng với biểu đồ hiệu suất.

### Hình ảnh Trực quan

| Tên thuật toán | Hình ảnh                   |
| -------------- | -------------------------- |
| BFS            | ![BFS](assets/BFS_2.gif)   |
| DFS            | ![DFS](assets/DFS.gif)     |
| UCS            | ![UCS](assets/UCS.gif)     |
| IDDFS          | ![IDDFS](assets/IDDFS.gif) |
