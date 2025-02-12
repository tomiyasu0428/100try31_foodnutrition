# 食品栄養アプリ処理フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant Flask as Flaskアプリ
    participant ImageProc as 画像処理
    participant Gemini as Gemini API
    participant GeminiTrans as Gemini 翻訳API
    participant Nutritionix as Nutritionix API
    
    User->>Flask: 食品画像をアップロード
    Flask->>ImageProc: 画像の前処理
    Note over ImageProc: リサイズ<br/>Base64エンコード
    
    ImageProc->>Gemini: 画像を送信
    Note over Gemini: 画像認識<br/>英語で食品名を特定
    Gemini-->>Flask: 英語の食品名を返す
    
    Flask->>GeminiTrans: 英語の食品名を送信
    Note over GeminiTrans: 日本語に翻訳
    GeminiTrans-->>Flask: 日本語の食品名を返す
    
    Flask->>Nutritionix: 英語の食品名で検索
    Note over Nutritionix: 栄養情報を検索<br/>- カロリー<br/>- タンパク質<br/>- 脂質<br/>- 炭水化物<br/>- ビタミン類<br/>- ミネラル類
    Nutritionix-->>Flask: 栄養情報を返す
    
    Flask->>Flask: 栄養情報を整形
    Note over Flask: カテゴリ分け<br/>- 基本情報<br/>- 主要栄養素<br/>- 詳細栄養素<br/>- ビタミン・ミネラル
    
    Flask-->>User: 結果を表示
    Note over User: Bootstrap UIで<br/>見やすく表示
```

## 処理の詳細説明

1. **画像アップロード & 前処理**
   - ユーザーが食品の画像をアップロード
   - 画像を適切なサイズにリサイズ
   - Base64エンコードしてAPI送信用に変換

2. **食品認識（Gemini API）**
   - 画像から食品を認識
   - 英語で食品名を返す（Nutritionix API用）
   - プロンプト: "Look at this food image and tell me what it is in English"

3. **翻訳処理（Gemini API）**
   - 英語の食品名を日本語に翻訳
   - ユーザー表示用の日本語名を生成

4. **栄養情報取得（Nutritionix API）**
   - 英語の食品名で栄養データベースを検索
   - 詳細な栄養情報を取得

5. **データ整形 & 表示**
   - 栄養情報を4つのカテゴリに分類
   - Bootstrap UIで見やすく表示
   - 適切な単位を付加（g, kcal, mg, %）
