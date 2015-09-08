reports = {}
reports['Detalles Inventario Fisico - Costo'] = '''object ppReport: TppReport
  AutoStop = False
  DataPipeline = daFIBQueryDataView1.Log_Inventario_Fisico
  PrinterSetup.BinName = 'Default'
  PrinterSetup.DocumentName = 'Report'
  PrinterSetup.PaperName = 'Letter'
  PrinterSetup.PrinterName = 'Default'
  PrinterSetup.mmMarginBottom = 6350
  PrinterSetup.mmMarginLeft = 6350
  PrinterSetup.mmMarginRight = 6350
  PrinterSetup.mmMarginTop = 6350
  PrinterSetup.mmPaperHeight = 279401
  PrinterSetup.mmPaperWidth = 215900
  PrinterSetup.PaperSize = 1
  SaveAsTemplate = True
  Template.DatabaseSettings.DataPipeline = plRBItem
  Template.DatabaseSettings.Name = 'Detalles Inventario Fisico - Costo'
  Template.DatabaseSettings.NameField = 'NAME'
  Template.DatabaseSettings.TemplateField = 'TEMPLATE'
  Template.SaveTo = stDatabase
  Template.Format = ftASCII
  Units = utScreenPixels
  AllowPrintToFile = True
  DeviceType = 'Screen'
  EmailSettings.ReportFormat = 'PDF'
  Language = lgSpanishMexico
  OutlineSettings.CreateNode = True
  OutlineSettings.CreatePageNodes = True
  OutlineSettings.Enabled = False
  OutlineSettings.Visible = False
  TextSearchSettings.DefaultString = '<HallarTexto>'
  TextSearchSettings.Enabled = False
  Left = 4
  Top = 208
  Version = '10.08'
  mmColumnWidth = 0
  DataPipelineName = 'Log_Inventario_Fisico'
  object ppHeaderBand1: TppHeaderBand
    mmBottomOffset = 0
    mmHeight = 13494
    mmPrintPosition = 0
    object ppLabel1: TppLabel
      UserName = 'Label1'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Articulo'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      Transparent = True
      mmHeight = 4191
      mmLeft = 1323
      mmTop = 9260
      mmWidth = 19315
      BandType = 0
    end
    object ppLabel2: TppLabel
      UserName = 'Label2'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Inicial'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 4191
      mmLeft = 52917
      mmTop = 9260
      mmWidth = 13494
      BandType = 0
    end
    object ppLabel3: TppLabel
      UserName = 'Label3'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Final'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 4191
      mmLeft = 71967
      mmTop = 9260
      mmWidth = 15610
      BandType = 0
    end
    object ppLabel4: TppLabel
      UserName = 'Label4'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Diferencia'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 4191
      mmLeft = 91017
      mmTop = 9260
      mmWidth = 21431
      BandType = 0
    end
    object ppLabel5: TppLabel
      UserName = 'Label5'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Detalle de inventario fisico - Costo'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Name = 'Arial'
      Font.Size = 14
      Font.Style = [fsBold]
      TextAlignment = taCentered
      Transparent = True
      mmHeight = 5821
      mmLeft = 52123
      mmTop = 265
      mmWidth = 95515
      BandType = 0
    end
    object ppLabel6: TppLabel
      UserName = 'Label6'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Precio Costo'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      Transparent = True
      mmHeight = 4233
      mmLeft = 119063
      mmTop = 9260
      mmWidth = 21431
      BandType = 0
    end
    object ppLabel7: TppLabel
      UserName = 'Label7'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Diferencia $'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      Transparent = True
      mmHeight = 4233
      mmLeft = 147902
      mmTop = 9260
      mmWidth = 21431
      BandType = 0
    end
  end
  object ppDetailBand1: TppDetailBand
    mmBottomOffset = 0
    mmHeight = 3175
    mmPrintPosition = 0
    object ppDBText1: TppDBText
      UserName = 'DBText1'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      DataField = 'NOMBRE'
      DataPipeline = daFIBQueryDataView1.Log_Inventario_Fisico
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      Transparent = True
      DataPipelineName = 'Log_Inventario_Fisico'
      mmHeight = 3260
      mmLeft = 1323
      mmTop = 0
      mmWidth = 47096
      BandType = 4
    end
    object ppDBText2: TppDBText
      UserName = 'DBText2'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      DataField = 'EXISTENCIA_INICIAL'
      DataPipeline = daFIBQueryDataView1.Log_Inventario_Fisico
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      DataPipelineName = 'Log_Inventario_Fisico'
      mmHeight = 3260
      mmLeft = 51065
      mmTop = 0
      mmWidth = 15346
      BandType = 4
    end
    object ppDBText3: TppDBText
      UserName = 'DBText3'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      DataField = 'EXISTENCIA_FINAL'
      DataPipeline = daFIBQueryDataView1.Log_Inventario_Fisico
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      DataPipelineName = 'Log_Inventario_Fisico'
      mmHeight = 3260
      mmLeft = 72496
      mmTop = 0
      mmWidth = 15081
      BandType = 4
    end
    object ppVariable1: TppVariable
      UserName = 'vDiferiencia'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      BlankWhenZero = False
      CalcOrder = 0
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 3260
      mmLeft = 97631
      mmTop = 0
      mmWidth = 14774
      BandType = 4
    end
    object ppVariable2: TppVariable
      UserName = 'vCosto'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      BlankWhenZero = False
      CalcOrder = 1
      DataType = dtCurrency
      DisplayFormat = '$#,0.00;-$#,0.00'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 3260
      mmLeft = 131689
      mmTop = 0
      mmWidth = 8805
      BandType = 4
    end
    object ppVariable3: TppVariable
      UserName = 'vDiferenciaDinero'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      BlankWhenZero = False
      CalcOrder = 2
      DataType = dtCurrency
      DisplayFormat = '$#,0.00;-$#,0.00'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 3260
      mmLeft = 146981
      mmTop = 0
      mmWidth = 22437
      BandType = 4
    end
  end
  object ppFooterBand1: TppFooterBand
    mmBottomOffset = 0
    mmHeight = 0
    mmPrintPosition = 0
  end
  object daDataModule1: TdaDataModule
    object daFIBQueryDataView1: TdaFIBQueryDataView
      UserName = 'Query_Log_Inventario_Fisico'
      Height = 298
      Left = 10
      NameColumnWidth = 105
      SizeColumnWidth = 35
      SortMode = 0
      Top = 10
      TypeColumnWidth = 52
      Width = 373
      AutoSearchTabOrder = 0
      object Log_Inventario_Fisico: TppChildDBPipeline
        AutoCreateFields = False
        UserName = 'Log_Inventario_Fisico'
        object ppField1: TppField
          FieldAlias = 'ARTICULO_ID'
          FieldName = 'ARTICULO_ID'
          FieldLength = 0
          DataType = dtInteger
          DisplayWidth = 10
          Position = 0
        end
        object ppField2: TppField
          FieldAlias = 'NOMBRE'
          FieldName = 'NOMBRE'
          FieldLength = 100
          DisplayWidth = 100
          Position = 1
        end
        object ppField3: TppField
          FieldAlias = 'EXISTENCIA_INICIAL'
          FieldName = 'EXISTENCIA_INICIAL'
          FieldLength = 0
          DataType = dtDouble
          DisplayWidth = 10
          Position = 2
        end
        object ppField4: TppField
          FieldAlias = 'EXISTENCIA_FINAL'
          FieldName = 'EXISTENCIA_FINAL'
          FieldLength = 0
          DataType = dtDouble
          DisplayWidth = 10
          Position = 3
        end
        object ppField5: TppField
          FieldAlias = 'COSTO_ULTIMA_COMPRA'
          FieldName = 'COSTO_ULTIMA_COMPRA'
          FieldLength = 0
          DataType = dtDouble
          DisplayWidth = 10
          Position = 4
        end
      end
      object daSQL1: TdaSQL
        CollationType = ctASCII
        DatabaseName = 'dtbsMicrosip'
        DatabaseType = dtInterBase
        DataPipelineName = 'Log_Inventario_Fisico'
        EditSQLAsText = True
        IsCaseSensitive = True
        LinkColor = clBlack
        MaxSQLFieldAliasLength = 0
        SQLText.Strings = (
          'SELECT ARTICULOS_1.ARTICULO_ID, ARTICULOS_1.NOMBRE, '
          
            '       SIC_LOGINVENTARIO_VALOR_INICIAL_1.EXISTENCIA as existenci' +
            'a_inicial, '
          
            '       (select INV_FIN_UNID from orsp_in_aux_art(ARTICULOS_1.ART' +
            'ICULO_ID , ALMACENES_1.NOMBRE, extract(year from current_date)||' +
            #39'/01/01'#39', extract(year from current_date)|| '#39'/12/31'#39','#39'S'#39','#39'N'#39')) a' +
            's existencia_final, ARTICULOS_1.COSTO_ULTIMA_COMPRA'
          'FROM SIC_LOGINVENTARIO SIC_LOGINVENTARIO_1'
          
            '      INNER JOIN SIC_LOGINVENTARIO_VALOR_INICIAL SIC_LOGINVENTAR' +
            'IO_VALOR_INICIAL_1 ON '
          
            '     (SIC_LOGINVENTARIO_VALOR_INICIAL_1.LOG_INVENTARIO_ID = SIC_' +
            'LOGINVENTARIO_1.ID)'
          '      INNER JOIN ARTICULOS ARTICULOS_1 ON '
          
            '     (ARTICULOS_1.ARTICULO_ID = SIC_LOGINVENTARIO_VALOR_INICIAL_' +
            '1.ARTICULO_ID)'
          '      INNER JOIN ALMACENES ALMACENES_1 ON '
          '     (ALMACENES_1.ALMACEN_ID = SIC_LOGINVENTARIO_1.ALMACEN_ID)'
          'where SIC_LOGINVENTARIO_1.id= :inventario_log_id')
        SQLType = sqSQL2
        object daField1: TdaField
          Alias = 'ARTICULO_ID'
          DataType = dtInteger
          DisplayWidth = 10
          FieldAlias = 'ARTICULO_ID'
          FieldLength = 0
          FieldName = 'ARTICULO_ID'
          SQLFieldName = 'ARTICULO_ID'
        end
        object daField2: TdaField
          Alias = 'NOMBRE'
          DisplayWidth = 100
          FieldAlias = 'NOMBRE'
          FieldLength = 100
          FieldName = 'NOMBRE'
          SQLFieldName = 'NOMBRE'
        end
        object daField3: TdaField
          Alias = 'EXISTENCIA_INICIAL'
          DataType = dtDouble
          DisplayWidth = 10
          FieldAlias = 'EXISTENCIA_INICIAL'
          FieldLength = 0
          FieldName = 'EXISTENCIA_INICIAL'
          SQLFieldName = 'EXISTENCIA_INICIAL'
        end
        object daField4: TdaField
          Alias = 'EXISTENCIA_FINAL'
          DataType = dtDouble
          DisplayWidth = 10
          FieldAlias = 'EXISTENCIA_FINAL'
          FieldLength = 0
          FieldName = 'EXISTENCIA_FINAL'
          SQLFieldName = 'EXISTENCIA_FINAL'
        end
        object daField5: TdaField
          Alias = 'COSTO_ULTIMA_COMPRA'
          DataType = dtDouble
          DisplayWidth = 10
          FieldAlias = 'COSTO_ULTIMA_COMPRA'
          FieldLength = 0
          FieldName = 'COSTO_ULTIMA_COMPRA'
          SQLFieldName = 'COSTO_ULTIMA_COMPRA'
        end
      end
    end
  end
  object raCodeModule1: TraCodeModule
    ProgramStream = {
      01060F5472614576656E7448616E646C65720B50726F6772616D4E616D650612
      76446966657269656E6369614F6E43616C630B50726F6772616D54797065070B
      747450726F63656475726506536F7572636506AA70726F636564757265207644
      6966657269656E6369614F6E43616C63287661722056616C75653A2056617269
      616E74293B0D0A626567696E0D0A0D0A202056616C7565203A3D204C6F675F49
      6E76656E746172696F5F46697369636F5B274558495354454E4349415F46494E
      414C275D20202D204C6F675F496E76656E746172696F5F46697369636F5B2745
      58495354454E4349415F494E494349414C275D3B0D0A0D0A656E643B0D0A0D43
      6F6D706F6E656E744E616D65060C76446966657269656E636961094576656E74
      4E616D6506064F6E43616C63074576656E74494402210001060F547261457665
      6E7448616E646C65720B50726F6772616D4E616D65060C76436F73746F4F6E43
      616C630B50726F6772616D54797065070B747450726F63656475726506536F75
      7263650CAB01000070726F6365647572652076436F73746F4F6E43616C632876
      61722056616C75653A2056617269616E74293B0D0A626567696E0D0A0D0A2020
      56616C7565203A3D204C6F675F496E76656E746172696F5F46697369636F5B27
      434F53544F5F554C54494D415F434F4D505241275D3B0D0A20200D0A20207644
      69666572656E63696144696E65726F2E56616C7565203A3D20284C6F675F496E
      76656E746172696F5F46697369636F5B274558495354454E4349415F46494E41
      4C275D20202D204C6F675F496E76656E746172696F5F46697369636F5B274558
      495354454E4349415F494E494349414C275D29202A2056616C75653B0D0A0D0A
      2020696628764469666572656E63696144696E65726F2E56616C75653C302974
      68656E0D0A2020626567696E0D0A20202020764469666572656E63696144696E
      65726F2E466F6E742E436F6C6F72203A3D20636C5265643B0D0A2020656E640D
      0A2020656C73650D0A2020626567696E0D0A20202020764469666572656E6369
      6144696E65726F2E466F6E742E436F6C6F72203A3D20636C57696E646F775465
      78743B0D0A2020656E643B0D0A656E643B0D0A0D436F6D706F6E656E744E616D
      65060676436F73746F094576656E744E616D6506064F6E43616C63074576656E
      74494402210000}
  end
  object ppParameterList1: TppParameterList
  end
end
'''

reports['Detalles Inventario Fisico - Precio de Venta'] = '''object ppReport: TppReport
  AutoStop = False
  DataPipeline = daFIBQueryDataView1.Log_Inventario_Fisico
  PrinterSetup.BinName = 'Default'
  PrinterSetup.DocumentName = 'Report'
  PrinterSetup.PaperName = 'Letter'
  PrinterSetup.PrinterName = 'Default'
  PrinterSetup.mmMarginBottom = 6350
  PrinterSetup.mmMarginLeft = 6350
  PrinterSetup.mmMarginRight = 6350
  PrinterSetup.mmMarginTop = 6350
  PrinterSetup.mmPaperHeight = 279401
  PrinterSetup.mmPaperWidth = 215900
  PrinterSetup.PaperSize = 1
  SaveAsTemplate = True
  Template.DatabaseSettings.DataPipeline = plRBItem
  Template.DatabaseSettings.Name = 'Detalles Inventario Fisico'
  Template.DatabaseSettings.NameField = 'NAME'
  Template.DatabaseSettings.TemplateField = 'TEMPLATE'
  Template.SaveTo = stDatabase
  Template.Format = ftASCII
  Units = utScreenPixels
  AllowPrintToFile = True
  DeviceType = 'Screen'
  EmailSettings.ReportFormat = 'PDF'
  Language = lgSpanishMexico
  OutlineSettings.CreateNode = True
  OutlineSettings.CreatePageNodes = True
  OutlineSettings.Enabled = False
  OutlineSettings.Visible = False
  TextSearchSettings.DefaultString = '<HallarTexto>'
  TextSearchSettings.Enabled = False
  Left = 4
  Top = 208
  Version = '10.08'
  mmColumnWidth = 0
  DataPipelineName = 'Log_Inventario_Fisico'
  object ppHeaderBand1: TppHeaderBand
    mmBottomOffset = 0
    mmHeight = 13494
    mmPrintPosition = 0
    object ppLabel1: TppLabel
      UserName = 'Label1'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Articulo'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      Transparent = True
      mmHeight = 4191
      mmLeft = 1323
      mmTop = 9260
      mmWidth = 19315
      BandType = 0
    end
    object ppLabel2: TppLabel
      UserName = 'Label2'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Inicial'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 4191
      mmLeft = 52917
      mmTop = 9260
      mmWidth = 13494
      BandType = 0
    end
    object ppLabel3: TppLabel
      UserName = 'Label3'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Final'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 4191
      mmLeft = 71967
      mmTop = 9260
      mmWidth = 15610
      BandType = 0
    end
    object ppLabel4: TppLabel
      UserName = 'Label4'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Diferencia'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 4191
      mmLeft = 91017
      mmTop = 9260
      mmWidth = 21431
      BandType = 0
    end
    object ppLabel5: TppLabel
      UserName = 'Label5'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Detalle de inventario fisico - Precio de venta'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Name = 'Arial'
      Font.Size = 14
      Font.Style = [fsBold]
      Transparent = True
      mmHeight = 5821
      mmLeft = 44715
      mmTop = 265
      mmWidth = 108479
      BandType = 0
    end
    object ppLabel6: TppLabel
      UserName = 'Label6'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Precio Venta'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      Transparent = True
      mmHeight = 4233
      mmLeft = 119063
      mmTop = 9260
      mmWidth = 21431
      BandType = 0
    end
    object ppLabel7: TppLabel
      UserName = 'Label7'
      AutoSize = False
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Diferencia $'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 10
      Font.Style = [fsBold]
      Transparent = True
      mmHeight = 4233
      mmLeft = 147902
      mmTop = 9260
      mmWidth = 21431
      BandType = 0
    end
  end
  object ppDetailBand1: TppDetailBand
    mmBottomOffset = 0
    mmHeight = 3175
    mmPrintPosition = 0
    object ppDBText1: TppDBText
      UserName = 'DBText1'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      DataField = 'NOMBRE'
      DataPipeline = daFIBQueryDataView1.Log_Inventario_Fisico
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      Transparent = True
      DataPipelineName = 'Log_Inventario_Fisico'
      mmHeight = 3260
      mmLeft = 1323
      mmTop = 0
      mmWidth = 47096
      BandType = 4
    end
    object ppDBText2: TppDBText
      UserName = 'DBText2'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      DataField = 'EXISTENCIA_INICIAL'
      DataPipeline = daFIBQueryDataView1.Log_Inventario_Fisico
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      DataPipelineName = 'Log_Inventario_Fisico'
      mmHeight = 3260
      mmLeft = 51065
      mmTop = 0
      mmWidth = 15346
      BandType = 4
    end
    object ppDBText3: TppDBText
      UserName = 'DBText3'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      DataField = 'EXISTENCIA_FINAL'
      DataPipeline = daFIBQueryDataView1.Log_Inventario_Fisico
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      DataPipelineName = 'Log_Inventario_Fisico'
      mmHeight = 3260
      mmLeft = 72496
      mmTop = 0
      mmWidth = 15081
      BandType = 4
    end
    object ppVariable1: TppVariable
      UserName = 'vDiferiencia'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      BlankWhenZero = False
      CalcOrder = 0
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 3260
      mmLeft = 97631
      mmTop = 0
      mmWidth = 14774
      BandType = 4
    end
    object ppVariable2: TppVariable
      UserName = 'vPrecioVenta'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      BlankWhenZero = False
      CalcOrder = 1
      DataType = dtCurrency
      DisplayFormat = '$#,0.00;-$#,0.00'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 3260
      mmLeft = 123815
      mmTop = 0
      mmWidth = 16679
      BandType = 4
    end
    object ppVariable3: TppVariable
      UserName = 'vDiferenciaDinero'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      BlankWhenZero = False
      CalcOrder = 2
      DataType = dtCurrency
      DisplayFormat = '$#,0.00;-$#,0.00'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Name = 'Arial'
      Font.Size = 8
      Font.Style = []
      TextAlignment = taRightJustified
      Transparent = True
      mmHeight = 3260
      mmLeft = 146981
      mmTop = 0
      mmWidth = 22437
      BandType = 4
    end
  end
  object ppFooterBand1: TppFooterBand
    mmBottomOffset = 0
    mmHeight = 0
    mmPrintPosition = 0
  end
  object daDataModule1: TdaDataModule
    object daFIBQueryDataView1: TdaFIBQueryDataView
      UserName = 'Query_Log_Inventario_Fisico'
      Height = 298
      Left = 10
      NameColumnWidth = 105
      SizeColumnWidth = 35
      SortMode = 0
      Top = 10
      TypeColumnWidth = 52
      Width = 373
      AutoSearchTabOrder = 0
      object Log_Inventario_Fisico: TppChildDBPipeline
        AutoCreateFields = False
        UserName = 'Log_Inventario_Fisico'
        object ppField1: TppField
          FieldAlias = 'ARTICULO_ID'
          FieldName = 'ARTICULO_ID'
          FieldLength = 0
          DataType = dtInteger
          DisplayWidth = 10
          Position = 0
        end
        object ppField2: TppField
          FieldAlias = 'NOMBRE'
          FieldName = 'NOMBRE'
          FieldLength = 100
          DisplayWidth = 100
          Position = 1
        end
        object ppField3: TppField
          FieldAlias = 'EXISTENCIA_INICIAL'
          FieldName = 'EXISTENCIA_INICIAL'
          FieldLength = 0
          DataType = dtDouble
          DisplayWidth = 10
          Position = 2
        end
        object ppField4: TppField
          FieldAlias = 'EXISTENCIA_FINAL'
          FieldName = 'EXISTENCIA_FINAL'
          FieldLength = 0
          DataType = dtDouble
          DisplayWidth = 10
          Position = 3
        end
      end
      object daSQL1: TdaSQL
        CollationType = ctASCII
        DatabaseName = 'dtbsMicrosip'
        DatabaseType = dtInterBase
        DataPipelineName = 'Log_Inventario_Fisico'
        EditSQLAsText = True
        IsCaseSensitive = True
        LinkColor = clBlack
        MaxSQLFieldAliasLength = 0
        SQLText.Strings = (
          'SELECT ARTICULOS_1.ARTICULO_ID, ARTICULOS_1.NOMBRE, '
          
            '       SIC_LOGINVENTARIO_VALOR_INICIAL_1.EXISTENCIA as existenci' +
            'a_inicial, '
          
            '       (select INV_FIN_UNID from orsp_in_aux_art(ARTICULOS_1.ART' +
            'ICULO_ID , ALMACENES_1.NOMBRE, extract(year from current_date)||' +
            #39'/01/01'#39', extract(year from current_date)|| '#39'/12/31'#39','#39'S'#39','#39'N'#39')) a' +
            's existencia_final'
          'FROM SIC_LOGINVENTARIO SIC_LOGINVENTARIO_1'
          
            '      INNER JOIN SIC_LOGINVENTARIO_VALOR_INICIAL SIC_LOGINVENTAR' +
            'IO_VALOR_INICIAL_1 ON '
          
            '     (SIC_LOGINVENTARIO_VALOR_INICIAL_1.LOG_INVENTARIO_ID = SIC_' +
            'LOGINVENTARIO_1.ID)'
          '      INNER JOIN ARTICULOS ARTICULOS_1 ON '
          
            '     (ARTICULOS_1.ARTICULO_ID = SIC_LOGINVENTARIO_VALOR_INICIAL_' +
            '1.ARTICULO_ID)'
          '      INNER JOIN ALMACENES ALMACENES_1 ON '
          '     (ALMACENES_1.ALMACEN_ID = SIC_LOGINVENTARIO_1.ALMACEN_ID)'
          'where SIC_LOGINVENTARIO_1.id= :inventario_log_id')
        SQLType = sqSQL2
        object daField1: TdaField
          Alias = 'ARTICULO_ID'
          DataType = dtInteger
          DisplayWidth = 10
          FieldAlias = 'ARTICULO_ID'
          FieldLength = 0
          FieldName = 'ARTICULO_ID'
          SQLFieldName = 'ARTICULO_ID'
        end
        object daField2: TdaField
          Alias = 'NOMBRE'
          DisplayWidth = 100
          FieldAlias = 'NOMBRE'
          FieldLength = 100
          FieldName = 'NOMBRE'
          SQLFieldName = 'NOMBRE'
        end
        object daField3: TdaField
          Alias = 'EXISTENCIA_INICIAL'
          DataType = dtDouble
          DisplayWidth = 10
          FieldAlias = 'EXISTENCIA_INICIAL'
          FieldLength = 0
          FieldName = 'EXISTENCIA_INICIAL'
          SQLFieldName = 'EXISTENCIA_INICIAL'
        end
        object daField4: TdaField
          Alias = 'EXISTENCIA_FINAL'
          DataType = dtDouble
          DisplayWidth = 10
          FieldAlias = 'EXISTENCIA_FINAL'
          FieldLength = 0
          FieldName = 'EXISTENCIA_FINAL'
          SQLFieldName = 'EXISTENCIA_FINAL'
        end
      end
    end
  end
  object raCodeModule1: TraCodeModule
    ProgramStream = {
      01060F5472614576656E7448616E646C65720B50726F6772616D4E616D650612
      76446966657269656E6369614F6E43616C630B50726F6772616D54797065070B
      747450726F63656475726506536F7572636506AA70726F636564757265207644
      6966657269656E6369614F6E43616C63287661722056616C75653A2056617269
      616E74293B0D0A626567696E0D0A0D0A202056616C7565203A3D204C6F675F49
      6E76656E746172696F5F46697369636F5B274558495354454E4349415F46494E
      414C275D20202D204C6F675F496E76656E746172696F5F46697369636F5B2745
      58495354454E4349415F494E494349414C275D3B0D0A0D0A656E643B0D0A0D43
      6F6D706F6E656E744E616D65060C76446966657269656E636961094576656E74
      4E616D6506064F6E43616C63074576656E74494402210001060F547261457665
      6E7448616E646C65720B50726F6772616D4E616D6506127650726563696F5665
      6E74614F6E43616C630B50726F6772616D54797065070B747450726F63656475
      726506536F757263650C6402000070726F636564757265207650726563696F56
      656E74614F6E43616C63287661722056616C75653A2056617269616E74293B0D
      0A626567696E0D0A20205365745175657279282753454C454354205052454349
      4F5F434F4E5F494D50554553544F2046524F4D205349435F4745545F50524543
      494F5F434F4E5F494D50554553544F283A4152544943554C4F5F49442927293B
      0D0A2020536574506172616D56616C756528274152544943554C4F5F4944272C
      204C6F675F496E76656E746172696F5F46697369636F5B274152544943554C4F
      5F4944275D20293B0D0A20204F70656E51756572793B0D0A202056616C756520
      3A3D204765744669656C644173466C6F6174282750524543494F5F434F4E5F49
      4D50554553544F27293B0D0A2020436C6F736551756572793B0D0A2020764469
      666572656E63696144696E65726F2E56616C7565203A3D20284C6F675F496E76
      656E746172696F5F46697369636F5B274558495354454E4349415F46494E414C
      275D20202D204C6F675F496E76656E746172696F5F46697369636F5B27455849
      5354454E4349415F494E494349414C275D29202A2056616C75653B0D0A0D0A20
      20696628764469666572656E63696144696E65726F2E56616C75653C30297468
      656E0D0A2020626567696E0D0A20202020764469666572656E63696144696E65
      726F2E466F6E742E436F6C6F72203A3D20636C5265643B0D0A2020656E640D0A
      2020656C73650D0A2020626567696E0D0A20202020764469666572656E636961
      44696E65726F2E466F6E742E436F6C6F72203A3D20636C57696E646F77546578
      743B0D0A2020656E643B0D0A656E643B0D0A0D436F6D706F6E656E744E616D65
      060C7650726563696F56656E7461094576656E744E616D6506064F6E43616C63
      074576656E74494402210001060F5472614576656E7448616E646C65720B5072
      6F6772616D4E616D650617764469666572656E63696144696E65726F4F6E4361
      6C630B50726F6772616D54797065070B747450726F63656475726506536F7572
      6365064B70726F63656475726520764469666572656E63696144696E65726F4F
      6E43616C63287661722056616C75653A2056617269616E74293B0D0A62656769
      6E0D0A0D0A0D0A0D0A656E643B0D0A0D436F6D706F6E656E744E616D65061176
      4469666572656E63696144696E65726F094576656E744E616D6506064F6E4361
      6C63074576656E74494402210000}
  end
  object ppParameterList1: TppParameterList
  end
end
'''
