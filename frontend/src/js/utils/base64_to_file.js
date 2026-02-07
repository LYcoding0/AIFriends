/**
 * 将Base64编码的字符串转换为File对象
 * 该函数解析Base64数据并创建对应的File对象，可用于文件上传等场景
 * 
 * @param {string} base64 - Base64编码的字符串，格式应为"data:mime/type;base64,encodedData"
 * @param {string} filename - 要创建的文件名
 * @returns {File} 返回创建的File对象
 * 
 * @example
 * const file = base64ToFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==", "image.png");
 */
export function base64ToFile(base64, filename) {
    // 解析Base64数据，分割MIME类型和编码数据
    const arr = base64.split(',')
    const mime = arr[0].match(/:(.*?);/)[1]
    
    // 解码Base64数据
    const bstr = atob(arr[1])
    let n = bstr.length
    
    // 创建字节数组
    const u8arr = new Uint8Array(n)
    while (n--) u8arr[n] = bstr.charCodeAt(n)
    
    // 创建并返回File对象
    return new File([u8arr], filename, {type: mime})
}