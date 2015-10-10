# Generated from FoostacheParser.g4 by ANTLR 4.5.1
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by FoostacheParser.

class FoostacheParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FoostacheParser#template.
    def visitTemplate(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#statements.
    def visitStatements(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#rawText.
    def visitRawText(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#literal.
    def visitLiteral(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#literalText.
    def visitLiteralText(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#stringField.
    def visitStringField(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#numberField.
    def visitNumberField(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#inlineFilter.
    def visitInlineFilter(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#numberFormat.
    def visitNumberFormat(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#ifBlock.
    def visitIfBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#ifTag.
    def visitIfTag(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#elseifBlock.
    def visitElseifBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#elseifTag.
    def visitElseifTag(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#elseBlock.
    def visitElseBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#orExpression.
    def visitOrExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#andExpression.
    def visitAndExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#boolExpression.
    def visitBoolExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#existsExpression.
    def visitExistsExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#notExpression.
    def visitNotExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#parenExpression.
    def visitParenExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#typeExpression.
    def visitTypeExpression(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#dotPath.
    def visitDotPath(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#caretPath.
    def visitCaretPath(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#idObjectKey.
    def visitIdObjectKey(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#qsObjectKey.
    def visitQsObjectKey(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#arrayIndex.
    def visitArrayIndex(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#withBlock.
    def visitWithBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateBlock.
    def visitIterateBlock(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#indexRange.
    def visitIndexRange(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#indexRangeB.
    def visitIndexRangeB(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#indexRangeC.
    def visitIndexRangeC(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateClause.
    def visitIterateClause(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateBeforeClause.
    def visitIterateBeforeClause(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateAfterClause.
    def visitIterateAfterClause(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateBetweenClause.
    def visitIterateBetweenClause(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#iterateElseClause.
    def visitIterateElseClause(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoostacheParser#filterBlock.
    def visitFilterBlock(self, ctx):
        return self.visitChildren(ctx)


