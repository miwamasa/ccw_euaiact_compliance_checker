# 背景
これは、EU AI法のコンプライアンスチェッカのロジックの最適化プロジェクトである

specifications/Theory.md    最適化の理論

src/decision_engine.py  決定エンジン
src/optimizer.py    最適化

## ユースケース１
これは以下のサイトにあるcompliance checkerを参考にしたユースケース
　https://artificialintelligenceact.eu/assessment/eu-ai-act-compliance-checker/


use_case1/original_checker_by_FutureInc.yaml   ロジックをyamlに落としたもの

use_case1/optimized_checker_by_FutureInc.yaml  最適化したもの

## ユースケース２
これは以下のサイトにあるcompliance checkerを参考にしたユースケース
　https://ai-act-service-desk.ec.europa.eu/en/eu-ai-act-compliance-checker

use_case2/checkerlogic_20260130.json　上記サイトにあるQ&Aロジック

# 指示
1)srcを用いてユースケース1を実行してコンパクト化を確認する
2)同様にユースケース2について、jsonをoriginalなyamlに展開し多雨で、ユースケース１と同様なコンパクト化を実施確認する

これらの過程でsrcに不具合が発生した場合はこれを修正し、汎用化を試みること。

最後に、use_case2において、日本語でコンプライアンスチェックのhtmlアプリを作成、このとき、逆引き、すなわち、決定木の最終的な結果（複数あるはず）から、それに至る、チェック項目やAI法の要求する義務がわかる逆引きモードもつけてほしい


ファイルの置き場はオリジナルから変えたので、README.mdに書いてあるパスとは異なることに注意。