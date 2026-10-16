# 教学材料

学生指导书为teacher_lab_guide.docx，课堂导入为lecture_slides.pptx（10页，宋体，逐项淡入）。Markdown、slides_plan.json及生成脚本同时保留。

学生运行实验只需根目录requirements.txt，不需要安装教学材料依赖。教师修改指导书后，可安装requirements-materials.txt并执行：

```bash
python materials/generate_materials.py --docx-only
```

重建PPT需本机Node和已配置的@oai/artifact-tool。设置RUNTIME_NODE与RUNTIME_NODE_MODULES后运行python materials/generate_materials.py，可重建Word与PPT。PPT脚本重新生成可编辑正文和数据图片，原生淡入动画为发布前Office处理；重建后若需要动画，教师在PowerPoint重新设置。

教师参考图来自examples/teacher_results，参数见其comparison.json。参考实现不随学生仓库发布。原课件/学生名单均未嵌入这两份教学材料。
