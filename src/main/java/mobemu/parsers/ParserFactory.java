package mobemu.parsers;

import mobemu.parsers.UPB.UpbTrace;
import mobemu.trace.Parser;

import java.util.Objects;

public class ParserFactory {

    private ParserFactory() {

    }
    private static class ParserFactoryHelper {
        private static final ParserFactory INSTANCE = new ParserFactory();
    }

    public static ParserFactory getInstance() {
        return ParserFactoryHelper.INSTANCE;
    }


    public Parser getParser(String type) {
        if (type.equals("Haggle-Intel")) {
            return new Haggle(Haggle.HaggleTrace.INTEL);
        } else if (type.equals("Haggle-Cambridge")) {
            return new Haggle(Haggle.HaggleTrace.CAMBRIDGE);
        } else if (type.equals("Haggle-Content")) {
            return new Haggle(Haggle.HaggleTrace.CONTENT);
        } else if (type.equals("Haggle-Content")) {
            return new Haggle(Haggle.HaggleTrace.INFOCOM2006);
        }  else if (type.equals("NCCU")) {
            return new NCCU();
        } else if (type.equals("Sigcomm")) {
            return new Sigcomm();
        } else if (type.equals("SocialBlueConn")) {
            return new SocialBlueConn();
        } else if (type.equals("StAndrews")) {
            return new StAndrews();
        } else if (type.equals("UPB2011")) {
            return new UPB(UpbTrace.UPB2011);
        } else if (type.equals("UPB2012")) {
            return new UPB(UpbTrace.UPB2012);
        } else if (type.equals("UPB2015")) {
            return new UPB(UpbTrace.UPB2015);
        } else {
            return null;
        }
    }

}
