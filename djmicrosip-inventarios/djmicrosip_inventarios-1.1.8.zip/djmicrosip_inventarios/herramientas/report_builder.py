reports = {}
reports['Detalles Inventario Fisico'] = '''object ppReport: TppReport
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
  Template.DatabaseSettings.Name = 'inventario detalles2'
  Template.DatabaseSettings.NameField = 'NAME'
  Template.DatabaseSettings.TemplateField = 'TEMPLATE'
  Template.FileName = 'C:\Users\Jesus\Desktop\DetalleInventarioLog.rtm'
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
    mmHeight = 13229
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
      mmLeft = 529
      mmTop = 8467
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
      Transparent = True
      mmHeight = 4191
      mmLeft = 50800
      mmTop = 8731
      mmWidth = 41804
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
      Transparent = True
      mmHeight = 4191
      mmLeft = 100542
      mmTop = 8467
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
      Transparent = True
      mmHeight = 4233
      mmLeft = 144198
      mmTop = 8731
      mmWidth = 21431
      BandType = 0
    end
    object ppLabel5: TppLabel
      UserName = 'Label5'
      Border.BorderPositions = []
      Border.Color = clBlack
      Border.Style = psSolid
      Border.Visible = False
      Caption = 'Detalle de inventario fisico'
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clBlack
      Font.Name = 'Arial'
      Font.Size = 14
      Font.Style = [fsBold]
      Transparent = True
      mmHeight = 5821
      mmLeft = 59002
      mmTop = 265
      mmWidth = 85196
      BandType = 0
    end
  end
  object ppDetailBand1: TppDetailBand
    mmBottomOffset = 0
    mmHeight = 4763
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
      Transparent = True
      DataPipelineName = 'Log_Inventario_Fisico'
      mmHeight = 3260
      mmLeft = 51065
      mmTop = 0
      mmWidth = 32808
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
      Transparent = True
      DataPipelineName = 'Log_Inventario_Fisico'
      mmHeight = 3260
      mmLeft = 100806
      mmTop = 0
      mmWidth = 32808
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
      Transparent = True
      mmHeight = 3260
      mmLeft = 144727
      mmTop = 0
      mmWidth = 14774
      BandType = 4
    end
  end
  object ppFooterBand1: TppFooterBand
    mmBottomOffset = 0
    mmHeight = 0
    mmPrintPosition = 0
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
      4E616D6506064F6E43616C63074576656E74494402210000}
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
          FieldAlias = 'NOMBRE'
          FieldName = 'NOMBRE'
          FieldLength = 100
          DisplayWidth = 100
          Position = 0
        end
        object ppField2: TppField
          FieldAlias = 'EXISTENCIA_INICIAL'
          FieldName = 'EXISTENCIA_INICIAL'
          FieldLength = 0
          DataType = dtDouble
          DisplayWidth = 10
          Position = 1
        end
        object ppField3: TppField
          FieldAlias = 'EXISTENCIA_FINAL'
          FieldName = 'EXISTENCIA_FINAL'
          FieldLength = 0
          DataType = dtDouble
          DisplayWidth = 10
          Position = 2
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
          'SELECT ARTICULOS_1.NOMBRE, '
          
            '       SIC_LOGINVENTARIO_VALOR_INICIAL_1.EXISTENCIA as existenci' +
            'a_inicial, '
          
            '       (select INV_FIN_UNID from orsp_in_aux_art(ARTICULOS_1.ART' +
            'ICULO_ID , ALMACENES_1.NOMBRE, '#39'2015/01/01'#39','#39'2015/12/31'#39','#39'S'#39','#39'N'#39 +
            ')) as existencia_final'
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
          Alias = 'NOMBRE'
          DisplayWidth = 100
          FieldAlias = 'NOMBRE'
          FieldLength = 100
          FieldName = 'NOMBRE'
          SQLFieldName = 'NOMBRE'
        end
        object daField2: TdaField
          Alias = 'EXISTENCIA_INICIAL'
          DataType = dtDouble
          DisplayWidth = 10
          FieldAlias = 'EXISTENCIA_INICIAL'
          FieldLength = 0
          FieldName = 'EXISTENCIA_INICIAL'
          SQLFieldName = 'EXISTENCIA_INICIAL'
        end
        object daField3: TdaField
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
  object ppParameterList1: TppParameterList
  end
end
'''
