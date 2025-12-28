# 反爬虫机制说明

CPTools 已集成多层反爬虫机制，确保在大规模截图任务中不会被目标网站封禁。

## 🛡️ 已实现的反爬虫机制

### 1. 浏览器启动优化

使用轻量级浏览器参数，模拟真实用户环境：

```python
launch_args = [
    '--no-sandbox',
    '--disable-dev-shm-usage',          # 低内存环境
    '--disable-gpu',                     # 节省资源
    '--disable-software-rasterizer',
    '--disable-extensions',
    '--disable-background-networking',   # 减少后台请求
    '--disable-sync',
    '--disable-translate',
    '--enable-automation',
    '--password-store=basic',
    '--use-mock-keychain',
    # ... 更多优化参数
]
```

**作用**：
- ✅ 降低资源消耗
- ✅ 减少被识别为机器人的特征
- ✅ 提高稳定性

### 2. 随机延迟（模拟人类行为）⭐

每次请求前添加随机延迟：

```python
delay = random.uniform(1.5, 3.5)  # 1.5-3.5秒随机延迟
await asyncio.sleep(delay)
```

**作用**：
- ✅ 模拟真实用户浏览速度
- ✅ 避免短时间内大量请求
- ✅ 降低被识别为爬虫的风险

**建议**：
- 快速模式：`1.0-2.0` 秒
- 正常模式：`1.5-3.5` 秒（默认）
- 保守模式：`3.0-6.0` 秒

### 3. 真实浏览器特征

设置完整的浏览器上下文：

```python
context = await browser.new_context(
    viewport={'width': width, 'height': height},
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    locale='en-US',
    ignore_https_errors=True,
)
```

**作用**：
- ✅ 真实的 User-Agent
- ✅ 标准视口大小
- ✅ 设置语言环境
- ✅ 忽略 HTTPS 证书错误

### 4. 智能页面加载策略

使用 `domcontentloaded` 而不是完全加载：

```python
# 不等待所有资源加载完成
await page.goto(url, wait_until='domcontentloaded')

# 尝试等待网络空闲，但不强制
try:
    await page.wait_for_load_state('networkidle', timeout=3000)
except:
    pass  # 超时不影响截图
```

**作用**：
- ✅ 更快的加载速度
- ✅ 更像真实用户（不等待所有广告/追踪脚本）
- ✅ 减少请求被中断的风险

### 5. HTTP 状态码检查

在截图前检查页面状态：

```python
if resp is not None and resp.status >= 400:
    # 记录错误，不浪费资源截图
    return {'status': 'failed', 'error': f'HTTP {resp.status}'}
```

**作用**：
- ✅ 避免对错误页面截图
- ✅ 快速识别访问问题
- ✅ 节省资源

### 6. 轻量级截图配置

可选的性能优化（注释中提供）：

```python
# 方式1: 使用 JPEG + 降低质量（更快，更小）
await page.screenshot(
    path=str(screenshot_path),
    full_page=True,
    type='jpeg',
    quality=80
)

# 方式2: 只截取视口（当前使用，更快）
await page.screenshot(
    path=str(screenshot_path),
    full_page=False  # 只截可见区域
)
```

**作用**：
- ✅ 减少内存占用
- ✅ 加快截图速度
- ✅ 减小文件大小

## 📊 参数调优建议

### 并发数设置

根据目标网站调整并发数：

```bash
# 保守模式（避免被封）
cptools screenshot ... -c 2

# 正常模式（推荐）
cptools screenshot ... -c 5

# 激进模式（风险较高）
cptools screenshot ... -c 10
```

**建议**：
- 🐌 慢速/严格网站：`-c 2` + 延迟 3-6秒
- 🚶 一般网站：`-c 5` + 延迟 1.5-3.5秒（默认）
- 🏃 宽松网站：`-c 10` + 延迟 1-2秒

### 超时时间设置

```bash
# 快速响应网站
cptools screenshot ... --timeout 15000  # 15秒

# 一般网站
cptools screenshot ... --timeout 30000  # 30秒（默认）

# 慢速网站
cptools screenshot ... --timeout 60000  # 60秒
```

## 🎯 最佳实践

### 1. 分批执行大量任务

```bash
# 不推荐：一次性处理1000个URL
cptools screenshot --csv 1000_urls.csv -c 10

# 推荐：分批处理
split -l 100 urls.csv batch_
for file in batch_*; do
    cptools screenshot --csv "$file" -c 5
    sleep 60  # 批次间休息60秒
done
```

### 2. 使用随机化参数

创建配置脚本：

```bash
#!/bin/bash
# 随机并发数（3-7之间）
CONCURRENCY=$((RANDOM % 5 + 3))

cptools screenshot \
  --host http://example.com \
  --csv data.csv \
  -c $CONCURRENCY
```

### 3. 错误重试策略

```bash
#!/bin/bash
MAX_RETRIES=3
RETRY=0

while [ $RETRY -lt $MAX_RETRIES ]; do
    cptools screenshot --csv data.csv -c 5
    
    if [ $? -eq 0 ]; then
        echo "成功！"
        break
    else
        RETRY=$((RETRY + 1))
        echo "失败，重试 $RETRY/$MAX_RETRIES"
        sleep $((RETRY * 30))  # 递增等待时间
    fi
done
```

### 4. 时间段分散

避免在同一时间段集中请求：

```bash
# 使用 cron 分散任务
# 每小时的不同时间点执行
0 9 * * * cptools screenshot --csv batch1.csv -c 3
30 9 * * * cptools screenshot --csv batch2.csv -c 3
0 10 * * * cptools screenshot --csv batch3.csv -c 3
```

## 🚨 风险提示

### 可能被识别为爬虫的情况

1. **并发过高** 
   - ❌ 短时间内大量并发请求
   - ✅ 限制并发数，添加延迟

2. **请求频率过快**
   - ❌ 毫秒级连续请求
   - ✅ 随机延迟 1-3 秒

3. **固定的访问模式**
   - ❌ 完全相同的时间间隔
   - ✅ 随机化延迟和批次

4. **UA 特征明显**
   - ❌ 默认 Playwright UA
   - ✅ 使用真实浏览器 UA（已配置）

### 如果被封禁

1. **降低并发数**
   ```bash
   cptools screenshot ... -c 1  # 单线程
   ```

2. **增加延迟**
   - 修改代码中的 `random.uniform(3.0, 6.0)`

3. **使用代理**（需要自行实现）
   ```python
   context = await browser.new_context(
       proxy={'server': 'http://proxy-server:port'}
   )
   ```

4. **更换 IP 地址**
   - 使用 VPN
   - 使用代理池

## 🔧 高级配置

### 自定义延迟范围

修改 `screenshot.py` 中的延迟参数：

```python
# 找到这行
delay = random.uniform(1.5, 3.5)

# 修改为
delay = random.uniform(3.0, 6.0)  # 更保守的延迟
```

### 添加请求头

在 `screenshot_single_page` 函数中：

```python
# 添加额外的请求头
await page.set_extra_http_headers({
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
})
```

### Cookie 管理

```python
# 保存 cookies
cookies = await context.cookies()
# 保存到文件...

# 加载 cookies
await context.add_cookies(cookies)
```

## 📈 性能 vs 安全平衡

| 配置 | 速度 | 安全性 | 适用场景 |
|------|------|--------|----------|
| `-c 10`, 延迟 1-2s | ⚡⚡⚡ | ⚠️ | 测试环境，宽松网站 |
| `-c 5`, 延迟 1.5-3.5s | ⚡⚡ | ✅ | 生产环境（默认）|
| `-c 2`, 延迟 3-6s | ⚡ | ✅✅✅ | 严格网站，避免封禁 |

## 🎓 总结

CPTools 的反爬虫机制平衡了以下因素：

1. ✅ **性能** - 足够快，支持批量处理
2. ✅ **安全** - 模拟真实用户，降低被封风险
3. ✅ **资源** - 优化内存和 CPU 使用
4. ✅ **稳定** - 容错机制，处理各种异常

**默认配置已经足够安全**，但根据目标网站的严格程度，你可以：
- 🔧 调整并发数 `-c`
- 🔧 修改延迟范围
- 🔧 分批执行任务

---

**需要帮助？** 查看 [完整文档](../README.md)

