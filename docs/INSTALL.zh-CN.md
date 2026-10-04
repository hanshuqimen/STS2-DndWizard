# 玩家安装与更新

适配：Windows《杀戮尖塔 2》v0.107.1，BaseLib 3.3.2。其他版本兼容性尚未验证。

1. 退出游戏并找到游戏安装文件夹。
2. 从 [BaseLib Releases](https://github.com/Alchyr/BaseLib-StS2/releases) 获取依赖并按其说明安装。本模组不附带 BaseLib。
3. 从 [本项目 Releases](https://github.com/hanshuqimen/STS2-DndWizard/releases/latest) 下载 DndWizard-v0.4.0-sts2-0.107.1.zip。
4. 把包内 DndWizard 文件夹放进游戏 mods 目录。最终路径应为 mods/DndWizard/DndWizard.dll，不要套两层 DndWizard。
5. 启动游戏，允许加载模组，新开一局选择法师。

更新时先关闭游戏，备份旧 mods/DndWizard 与自己的游戏存档，再替换上述三个模组文件。源码中的 Install.ps1 适用于构建后的产物，需通过 -GameDir 指定你的路径。

如果找不到角色：检查 BaseLib 是否安装，三个文件是否齐全，是否多嵌套一层文件夹，以及游戏版本是否匹配。若出现加载报错，请提交 Issue 并附版本和相关日志片段；发日志前删除用户名、个人路径及其他私人信息。

卸载时关闭游戏，将 mods/DndWizard 移至游戏目录外。法师对局存档继续游玩时需要本模组。

作者已手动测试最新版，未发现问题；建议用新对局体验。GitHub 的 Source code 下载只包含源码，玩家请下载专用安装包。
