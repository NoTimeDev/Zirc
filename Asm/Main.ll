; ModuleID = 'Asm/Test.c'
source_filename = "Asm/Test.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline nounwind optnone sspstrong uwtable
define dso_local i32 @Test(i32 noundef %0, i32 noundef %1) #0 !dbg !10 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
    #dbg_declare(ptr %3, !19, !DIExpression(), !20)
  store i32 %1, ptr %4, align 4
    #dbg_declare(ptr %4, !21, !DIExpression(), !22)
  %5 = load i32, ptr %3, align 4, !dbg !23
  %6 = load i32, ptr %4, align 4, !dbg !24
  %7 = add nsw i32 %5, %6, !dbg !25
  ret i32 %7, !dbg !26
}

; Function Attrs: noinline nounwind optnone sspstrong uwtable
define dso_local i32 @main() #0 !dbg !27 {
  %1 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  %2 = call i32 @Test(i32 noundef 1, i32 noundef 2), !dbg !30
  ret i32 %2, !dbg !31
}

attributes #0 = { noinline nounwind optnone sspstrong uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5, !6, !7, !8}
!llvm.ident = !{!9}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 19.1.7", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "Asm/Test.c", directory: "/home/devvy/Projects/Zirc", checksumkind: CSK_MD5, checksum: "6a97d6db48f8de0cb881bedb3ed20204")
!2 = !{i32 7, !"Dwarf Version", i32 5}
!3 = !{i32 2, !"Debug Info Version", i32 3}
!4 = !{i32 1, !"wchar_size", i32 4}
!5 = !{i32 8, !"PIC Level", i32 2}
!6 = !{i32 7, !"PIE Level", i32 2}
!7 = !{i32 7, !"uwtable", i32 2}
!8 = !{i32 7, !"frame-pointer", i32 2}
!9 = !{!"clang version 19.1.7"}
!10 = distinct !DISubprogram(name: "Test", scope: !1, file: !1, line: 2, type: !11, scopeLine: 2, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !18)
!11 = !DISubroutineType(types: !12)
!12 = !{!13, !17, !17}
!13 = !DIDerivedType(tag: DW_TAG_typedef, name: "int32_t", file: !14, line: 26, baseType: !15)
!14 = !DIFile(filename: "/usr/include/bits/stdint-intn.h", directory: "", checksumkind: CSK_MD5, checksum: "d8f6972fff852003b8782e6edd3802e7")
!15 = !DIDerivedType(tag: DW_TAG_typedef, name: "__int32_t", file: !16, line: 41, baseType: !17)
!16 = !DIFile(filename: "/usr/include/bits/types.h", directory: "", checksumkind: CSK_MD5, checksum: "0737a53e1b85eab0e0ba9675962d13f4")
!17 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!18 = !{}
!19 = !DILocalVariable(name: "x", arg: 1, scope: !10, file: !1, line: 2, type: !17)
!20 = !DILocation(line: 2, column: 18, scope: !10)
!21 = !DILocalVariable(name: "y", arg: 2, scope: !10, file: !1, line: 2, type: !17)
!22 = !DILocation(line: 2, column: 25, scope: !10)
!23 = !DILocation(line: 3, column: 12, scope: !10)
!24 = !DILocation(line: 3, column: 16, scope: !10)
!25 = !DILocation(line: 3, column: 14, scope: !10)
!26 = !DILocation(line: 3, column: 5, scope: !10)
!27 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 6, type: !28, scopeLine: 6, spFlags: DISPFlagDefinition, unit: !0)
!28 = !DISubroutineType(types: !29)
!29 = !{!13}
!30 = !DILocation(line: 7, column: 12, scope: !27)
!31 = !DILocation(line: 7, column: 5, scope: !27)
